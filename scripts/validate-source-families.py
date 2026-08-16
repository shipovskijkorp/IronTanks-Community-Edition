#!/usr/bin/env python3
"""Validate the BCCE-style shared/family/platform/target source architecture."""
from __future__ import annotations

import filecmp
import sys
from pathlib import Path

from source_layout import ROOT, load_properties, materialize_target, target_ids, target_layout, validate_all_directives


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def java_files(base: Path):
    root = base / "src/main/java"
    return list(root.rglob("*.java")) if root.is_dir() else []


def main() -> None:
    props = load_properties()
    targets = target_ids(props)
    validate_all_directives(props)

    shared = ROOT / "source-shared"
    families = ROOT / "source-families"
    platforms = ROOT / "source-platforms"
    overlays = ROOT / "version-src"
    for root in (shared, families, platforms, overlays):
        if not root.is_dir():
            fail(f"missing source root {root.relative_to(ROOT)}")

    # Shared and family layers may depend on Minecraft/BuildCraft, but never on a loader.
    for base in [shared, *(p for p in families.iterdir() if p.is_dir())]:
        for path in java_files(base):
            text = path.read_text(encoding="utf-8")
            if "net.minecraftforge." in text or "net.neoforged." in text:
                fail(f"loader import escaped platform layer: {path.relative_to(ROOT)}")

    # Target overlays are resources-only today; no source copy should sneak back in.
    for overlay in overlays.iterdir():
        if not overlay.is_dir():
            continue
        java_root = overlay / "src/main/java"
        if java_root.exists() and any(java_root.rglob("*.java")):
            fail(f"target overlay contains Java source: {overlay.relative_to(ROOT)}")

    # Byte-identical overrides are pointless and usually indicate an accidental copy.
    for target in targets:
        layout = target_layout(target, props)
        candidates: dict[str, list[Path]] = {}
        for layer in layout.layers:
            if not layer.exists():
                continue
            for path in layer.rglob("*"):
                if path.is_file() and path.name != ".gitkeep":
                    candidates.setdefault(path.relative_to(layer).as_posix(), []).append(path)
        for rel, paths in candidates.items():
            for left, right in zip(paths, paths[1:]):
                if filecmp.cmp(left, right, shallow=False):
                    fail(f"{target}: byte-identical override {rel} in {left.relative_to(ROOT)} and {right.relative_to(ROOT)}")

        output = ROOT / "build" / "validation-effective" / target
        materialize_target(target, output, props)
        actual_java = list((output / "src/main/java").rglob("*.java"))
        if len(actual_java) != 14:
            fail(f"{target}: expected 14 effective Java files, found {len(actual_java)}")
        for path in actual_java:
            text = path.read_text(encoding="utf-8")
            if "//?" in text or "/*?" in text:
                fail(f"{target}: unresolved Stonecutter directive in {path.relative_to(output)}")

    print("Source layering OK: shared + family + platform + target overlays materialize all targets")


if __name__ == "__main__":
    main()
