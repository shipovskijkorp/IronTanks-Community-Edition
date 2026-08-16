#!/usr/bin/env python3
"""Validate the independent legacy/modern Stonecutter build roots."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from source_layout import ROOT, generation_config_paths, generation_targets, load_properties, target_ids, target_layout

ACTIVE_RE = re.compile(r'^\s*stonecutter\s+active\s+"([^"]+)"', re.MULTILINE)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def prop(props: dict[str, str], target: str, key: str) -> str:
    value = props.get(f"target.{target}.{key}", props.get(f"common.{key}", "")).strip()
    if not value:
        fail(f"{target}: missing property {key}")
    return value


def wrapper_version(root: Path) -> str:
    path = root / "gradle/wrapper/gradle-wrapper.properties"
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    match = re.search(r"gradle-([0-9.]+)-bin\.zip", path.read_text(encoding="utf-8"))
    if not match:
        fail(f"cannot determine Gradle version from {path.relative_to(ROOT)}")
    return match.group(1)


def validate_generation(name: str, targets: list[str], props: dict[str, str]) -> str:
    root = generation_config_paths()[name].parent
    required = [
        "settings.gradle.kts", "stonecutter.gradle.kts", "targets.properties", "gradle.properties",
        "gradlew", "gradlew.bat", "gradle/wrapper/gradle-wrapper.jar", "gradle/wrapper/gradle-wrapper.properties",
    ]
    for rel in required:
        if not (root / rel).is_file():
            fail(f"{name}: missing {root.relative_to(ROOT) / rel}")

    settings = (root / "settings.gradle.kts").read_text(encoding="utf-8")
    controller = (root / "stonecutter.gradle.kts").read_text(encoding="utf-8")
    if 'file("../..").canonicalFile' not in settings:
        fail(f"{name}: settings does not resolve the repository root")
    if 'id("dev.kikugie.stonecutter") version "0.7.11"' not in settings:
        fail(f"{name}: Stonecutter 0.7.11 is not pinned")
    if 'kotlinController = true' not in settings:
        fail(f"{name}: kotlinController is not enabled")
    if 'tasks.register("buildAndCollect")' not in controller:
        fail(f"{name}: controller has no buildAndCollect task")

    active_match = ACTIVE_RE.search(controller)
    if not active_match or active_match.group(1) not in targets:
        fail(f"{name}: invalid active Stonecutter target")

    for target in targets:
        layout = target_layout(target, props)
        if layout.generation != name:
            fail(f"{target}: generation mismatch {layout.generation!r} != {name!r}")
        loader = target.rsplit('-', 1)[1]
        if layout.platform != loader:
            fail(f"{target}: source platform {layout.platform!r} != loader {loader!r}")
        if layout.family != name:
            fail(f"{target}: source family {layout.family!r} != generation {name!r}")
        for layer in layout.layers:
            if not layer.is_dir():
                fail(f"{target}: missing source layer {layer.relative_to(ROOT)}")

        script = root / f"build.{loader}.gradle"
        if not script.is_file():
            fail(f"{target}: missing {script.relative_to(ROOT)}")
        text = script.read_text(encoding="utf-8")
        for token in ("sourceLayoutScript", "prepareEffectiveSource", "effectiveSourceRoot", "buildAndCollect"):
            if token not in text:
                fail(f"{script.relative_to(ROOT)}: missing {token}")
        if loader == "forge" and "id 'net.minecraftforge.gradle' version '6.0.54'" not in text:
            fail(f"{script.relative_to(ROOT)}: ForgeGradle 6.0.54 is not pinned")
        if loader == "neoforge" and "id 'net.neoforged.moddev' version '2.0.143'" not in text:
            fail(f"{script.relative_to(ROOT)}: ModDevGradle 2.0.143 is not pinned")

        for key in (
            "deps.minecraft", "java.version", "source.root", "source.platform_root", "source.overlay_root",
            "loader.version_range", "minecraft.version_range", "buildcraft.version", "buildcraft.local_jar",
            "buildcraft.version_range", "pack.format", "pack.resource_format", "pack.data_format",
        ):
            prop(props, target, key)
        prop(props, target, "deps.forge" if loader == "forge" else "deps.neoforge")

    return wrapper_version(root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-targets", action="store_true")
    parser.add_argument("--generation", choices=tuple(generation_config_paths()))
    parser.add_argument("--loader")
    args = parser.parse_args()

    props = load_properties()
    targets = target_ids(props)
    generations = generation_targets(props)

    if args.list_targets:
        for target in targets:
            layout = target_layout(target, props)
            if args.generation and layout.generation != args.generation:
                continue
            if args.loader and layout.platform != args.loader:
                continue
            print(target)
        return

    if props.get("behaviorReference") != "1.19.2-forge":
        fail("behaviorReference must be 1.19.2-forge")

    for obsolete in (
        "settings.gradle.kts", "stonecutter.gradle.kts", "build.forge.gradle", "build.neoforge.gradle",
        "gradle.properties", "gradlew", "gradlew.bat", "gradle", "versions", "version-resources", "src",
    ):
        if (ROOT / obsolete).exists():
            fail(f"obsolete monolithic build/source path remains: {obsolete}")

    for name in ("build-all.sh", "build-all.ps1", "build-all.bat"):
        if not (ROOT / name).is_file():
            fail(f"missing build orchestrator {name}")

    required_targets = {"1.19.2-forge", "1.20.1-forge", "1.21.1-neoforge"}
    if set(targets) != required_targets:
        fail(f"production target matrix mismatch: {targets}")

    reports = []
    for generation, items in generations.items():
        reports.append(f"{generation}=Gradle {validate_generation(generation, items, props)} ({', '.join(items)})")
    print("Stonecutter build generations OK: " + "; ".join(reports))


if __name__ == "__main__":
    main()
