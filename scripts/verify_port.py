#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []

VERSIONS = {
    '1.19.2-forge': {
        'minecraft_version': '1.19.2',
        'forge_version': '43.5.0',
        'buildcraft_version': '8.0.12+1.19.2+forge',
        'java_version': '17',
        'pack': (9, 9, 10),
    },
    '1.20.1-forge': {
        'minecraft_version': '1.20.1',
        'forge_version': '47.4.10',
        'buildcraft_version': '8.0.11+1.20.1',
        'java_version': '17',
        'pack': (15, 15, 15),
    },
    '1.21.1-forge': {
        'minecraft_version': '1.21.1',
        'forge_version': '52.1.16',
        'buildcraft_version': '8.0.11+1.21.1+beta1',
        'java_version': '21',
        'pack': (34, 34, 48),
    },
    '1.21.1-neoforge': {
        'minecraft_version': '1.21.1',
        'neo_version': '21.1.244',
        'buildcraft_version': '8.0.11+b1+1.21.1+NeoForge',
        'java_version': '21',
        'pack': (34, 34, 48),
    },
}

TANKS = (
    'copper_tank', 'iron_tank', 'silver_tank', 'gold_tank', 'diamond_tank',
    'obsidian_tank', 'emerald_tank', 'aluminium_tank', 'stainlesssteel_tank',
    'titanium_tank', 'tungstensteel_tank', 'void_tank', 'creative_tank',
)
UPGRADES = (
    'glass_copper_upgrade', 'glass_iron_upgrade', 'copper_iron_upgrade',
    'copper_silver_upgrade', 'iron_gold_upgrade', 'silver_gold_upgrade',
    'gold_diamond_upgrade', 'diamond_obsidian_upgrade', 'diamond_emerald_upgrade',
    'diamond_aluminium_upgrade', 'emerald_stainlesssteel_upgrade',
    'aluminium_stainlesssteel_upgrade', 'stainlesssteel_titanium_upgrade',
    'titanium_tungstensteel_upgrade',
)
ITEMS = set(TANKS + UPGRADES)

STALE_LEGACY_SOURCES = (
    'com/indemnity83/irontanks/client/IronTanksClient.java',
    'com/indemnity83/irontanks/client/IronTanksClientForgeEvents.java',
    'com/indemnity83/irontanks/client/IronTanksClientRuntimeCompat.java',
    'com/indemnity83/irontanks/client/IronTanksClientScreens.java',
    'com/indemnity83/irontanks/client/gui/IronTanksTankComponent.java',
    'com/indemnity83/irontanks/client/gui/IronTanksTankScreen.java',
    'com/indemnity83/irontanks/common/menu/IronTanksTankMenu.java',
    'com/indemnity83/irontanks/common/registry/IronTanksGuis.java',
    'com/indemnity83/irontanks/common/registry/IronTanksMenus.java',
    'com/indemnity83/irontanks/common/util/IronTanksRuntimeCompat.java',
)

BLOCK_SPECS = {
    'COPPER_TANK': ('StackableTankBlock', 27, '4.0F', '2.0F'),
    'IRON_TANK': ('StackableTankBlock', 32, '5.0F', '3.0F'),
    'SILVER_TANK': ('StackableTankBlock', 43, '6.0F', '5.0F'),
    'GOLD_TANK': ('StackableTankBlock', 48, '7.0F', '4.0F'),
    'DIAMOND_TANK': ('StackableTankBlock', 64, '8.0F', '6.0F'),
    'OBSIDIAN_TANK': ('StackableTankBlock', 64, '50.0F', '1_200.0F'),
    'EMERALD_TANK': ('StackableTankBlock', 96, '8.0F', '6.0F'),
    'ALUMINIUM_TANK': ('StackableTankBlock', 96, '5.0F', '4.0F'),
    'STAINLESSSTEEL_TANK': ('StackableTankBlock', 128, '9.0F', '8.0F'),
    'TITANIUM_TANK': ('StackableTankBlock', 256, '10.0F', '10.0F'),
    'TUNGSTENSTEEL_TANK': ('StackableTankBlock', 512, '12.0F', '14.0F'),
    'VOID_TANK': ('VoidTankBlock', 8, '5.0F', '6.0F'),
    'CREATIVE_TANK': ('CreativeTankBlock', 1, None, None),
}

UPGRADE_SPECS = {
    'COPPER_IRON_UPGRADE': ('COPPER_TANK', 'IRON_TANK'),
    'COPPER_SILVER_UPGRADE': ('COPPER_TANK', 'SILVER_TANK'),
    'DIAMOND_OBSIDIAN_UPGRADE': ('DIAMOND_TANK', 'OBSIDIAN_TANK'),
    'GLASS_COPPER_UPGRADE': ('BCFactoryBlocks.TANK_BLOCK', 'COPPER_TANK'),
    'GLASS_IRON_UPGRADE': ('BCFactoryBlocks.TANK_BLOCK', 'IRON_TANK'),
    'GOLD_DIAMOND_UPGRADE': ('GOLD_TANK', 'DIAMOND_TANK'),
    'IRON_GOLD_UPGRADE': ('IRON_TANK', 'GOLD_TANK'),
    'SILVER_GOLD_UPGRADE': ('SILVER_TANK', 'GOLD_TANK'),
    'DIAMOND_EMERALD_UPGRADE': ('DIAMOND_TANK', 'EMERALD_TANK'),
    'DIAMOND_ALUMINIUM_UPGRADE': ('DIAMOND_TANK', 'ALUMINIUM_TANK'),
    'EMERALD_STAINLESSSTEEL_UPGRADE': ('EMERALD_TANK', 'STAINLESSSTEEL_TANK'),
    'ALUMINIUM_STAINLESSSTEEL_UPGRADE': ('ALUMINIUM_TANK', 'STAINLESSSTEEL_TANK'),
    'STAINLESSSTEEL_TITANIUM_UPGRADE': ('STAINLESSSTEEL_TANK', 'TITANIUM_TANK'),
    'TITANIUM_TUNGSTENSTEEL_UPGRADE': ('TITANIUM_TANK', 'TUNGSTENSTEEL_TANK'),
}


def fail(message: str) -> None:
    errors.append(message)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'Invalid JSON: {path.relative_to(ROOT)}: {exc}')
        return {}


def read_properties(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        result[key.strip()] = value.strip()
    return result


def condition_matches(expression: str, version: str, loader: str) -> bool:
    expression = expression.strip()
    if expression == 'neoforge':
        return loader == 'neoforge'
    if expression == 'forge':
        return loader == 'forge'
    match = re.fullmatch(r'(<=|>=|<|>)\s*(\d+)\.(\d+)(?:\.(\d+))?', expression)
    if not match:
        raise ValueError(f'Unsupported Stonecutter condition: {expression}')
    op, major, minor, patch = match.groups()
    target_tuple = tuple(int(part) for part in version.split('.'))
    while len(target_tuple) < 3:
        target_tuple += (0,)
    compare_tuple = (int(major), int(minor), int(patch or 0))
    return {
        '<': target_tuple < compare_tuple,
        '<=': target_tuple <= compare_tuple,
        '>': target_tuple > compare_tuple,
        '>=': target_tuple >= compare_tuple,
    }[op]


def render_stonecutter(text: str, version: str, loader: str) -> str:
    """Resolve the small Stonecutter directive subset used by this project."""
    output: list[str] = []
    stack: list[dict[str, Any]] = []

    def selected() -> bool:
        return all(frame['selected'] for frame in stack)

    for raw in text.splitlines():
        if_match = re.search(r'//\?\s*if\s+(.+?)\s*\{\s*$', raw)
        if if_match:
            result = condition_matches(if_match.group(1), version, loader)
            stack.append({'condition': result, 'selected': result, 'else': False})
            continue

        if re.search(r'//\?\}\s*else\s*\{\s*$', raw):
            if not stack:
                raise ValueError('Stonecutter else without if')
            stack[-1]['else'] = True
            stack[-1]['selected'] = not stack[-1]['condition']
            continue

        if re.search(r'//\?\}\s*$', raw):
            if not stack:
                raise ValueError('Stonecutter end without if')
            stack.pop()
            continue

        if not selected():
            continue

        line = raw
        # Selected branches can be stored inside a block comment in the VCS source.
        if line.lstrip().startswith('/*'):
            indent = line[:len(line) - len(line.lstrip())]
            line = indent + line.lstrip()[2:]
        if line.rstrip().endswith('*/'):
            line = line.rstrip()[:-2]
        output.append(line)

    if stack:
        raise ValueError('Unclosed Stonecutter condition')
    return '\n'.join(output) + '\n'


def strip_java_comments_and_strings(text: str) -> str:
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub('', text)


# Parse every JSON file.
json_files = list(ROOT.rglob('*.json'))
for path in json_files:
    read_json(path)

# Stonecutter project DSL and wrapper integrity.
settings = (ROOT / 'settings.gradle.kts').read_text(encoding='utf-8')
for node in VERSIONS:
    buildscript = 'build.neoforge.gradle' if node.endswith('neoforge') else 'build.forge.gradle'
    expected = f'version("{node}", "{VERSIONS[node]["minecraft_version"]}").buildscript("{buildscript}")'
    if expected not in settings:
        fail(f'Missing current Stonecutter buildscript DSL for {node}')
if '.buildscript =' in settings:
    fail('Obsolete Stonecutter buildscript assignment syntax remains')
if 'id("dev.kikugie.stonecutter") version "0.7.11"' not in settings:
    fail('Stonecutter 0.7.11 is not pinned in settings.gradle.kts')
if 'id("org.gradle.toolchains.foojay-resolver-convention") version "0.8.0"' not in settings:
    fail('Foojay toolchain resolver 0.8.0 is not pinned in settings.gradle.kts')
root_properties = read_properties(ROOT / 'gradle.properties')
if root_properties.get('dev.kikugie.stonecutter.hard_mode') != 'true':
    fail('Stonecutter hard_mode acknowledgement is missing')
stonecutter = (ROOT / 'stonecutter.gradle.kts').read_text(encoding='utf-8')
if 'stonecutter active "1.19.2-forge"' not in stonecutter:
    fail('Stonecutter active node is not declared with the current DSL')
if 'constants {' not in stonecutter or 'match(loader, "forge", "neoforge")' not in stonecutter:
    fail('Stonecutter loader constants are not configured')
if (ROOT / '.sc_active_version').exists():
    fail('Obsolete .sc_active_version file remains')
neo_build = (ROOT / 'build.neoforge.gradle').read_text(encoding='utf-8')
if "tasks.named('createMinecraftArtifacts')" not in neo_build or "dependsOn 'stonecutterGenerate'" not in neo_build:
    fail('NeoForge createMinecraftArtifacts is not ordered after stonecutterGenerate')
wrapper_jar = ROOT / 'gradle/wrapper/gradle-wrapper.jar'
wrapper_properties = ROOT / 'gradle/wrapper/gradle-wrapper.properties'
if not wrapper_jar.is_file():
    fail('Missing Gradle wrapper JAR')
else:
    wrapper_jar_sha = hashlib.sha256(wrapper_jar.read_bytes()).hexdigest()
    if wrapper_jar_sha != '91a239400bb638f36a1795d8fdf7939d532cdc7d794d1119b7261aac158b1e60':
        fail(f'Unexpected Gradle wrapper JAR checksum: {wrapper_jar_sha}')
if not wrapper_properties.is_file():
    fail('Missing Gradle wrapper properties')
else:
    wrapper = read_properties(wrapper_properties)
    expected_wrapper = r'https\://services.gradle.org/distributions/gradle-8.8-bin.zip'
    expected_distribution_sha = 'a4b4158601f8636cdeeab09bd76afb640030bb5b144aafe261a5e8af027dc612'
    if wrapper.get('distributionUrl') != expected_wrapper:
        fail(f'Gradle wrapper is {wrapper.get("distributionUrl")!r}, expected {expected_wrapper!r}')
    if wrapper.get('distributionSha256Sum') != expected_distribution_sha:
        fail('Gradle 8.8 distribution checksum is missing or incorrect')
forge_build = (ROOT / 'build.forge.gradle').read_text(encoding='utf-8')
if "id 'net.minecraftforge.gradle' version '6.0.54'" not in forge_build:
    fail('ForgeGradle 6.0.54 is not pinned in build.forge.gradle')
if "tasks.matching { it.name == 'reobfJar' }.configureEach" in forge_build:
    fail('Unsafe nested task-container reobfJar callback remains')
if "providers.gradleProperty('forge_reobf')" not in forge_build:
    fail('Forge reobf routing property is not read by build.forge.gradle')
if "jar.finalizedBy('reobfJar')" not in forge_build:
    fail('Legacy Forge jar is not finalized by reobfJar when enabled')
if 'forRepositories(fg.repository)' not in forge_build:
    fail('Modrinth exclusiveContent does not include ForgeGradle deobf repository')
for build_name in ('build.forge.gradle', 'build.neoforge.gradle'):
    build_text = (ROOT / build_name).read_text(encoding='utf-8')
    if 'def staleLegacySources = [' not in build_text or 'staleLegacySources.each { exclude it }' not in build_text:
        fail(f'{build_name}: Legacy source exclusion guard is missing')
    if "sourceSets.test.java {" not in build_text or "exclude 'buildcraft/**'" not in build_text:
        fail(f'{build_name}: Stale BuildCraft test-source exclusion guard is missing')
    if "sourceSets.test.resources {" not in build_text:
        fail(f'{build_name}: Stale BuildCraft test-resource exclusion guard is missing')
    if 'def versionResourceRootPath = versionResourceRoot.toPath().toAbsolutePath().normalize()' not in build_text:
        fail(f'{build_name}: Target-local resource root guard is missing')
    if 'sourcePath.startsWith(versionResourceRootPath)' not in build_text or 'details.exclude()' not in build_text:
        fail(f'{build_name}: Stale shared loader metadata exclusion is missing')

stale_test_root = ROOT / 'src/test'
if stale_test_root.exists():
    stale_buildcraft_tests = [p for p in stale_test_root.rglob('*') if p.is_file() and 'buildcraft' in p.parts]
    if stale_buildcraft_tests:
        fail('Stale BuildCraft tests remain in src/test: ' + ', '.join(str(p.relative_to(ROOT)) for p in stale_buildcraft_tests[:8]))

for stale_resource in (
    ROOT / 'src/main/resources/META-INF/mods.toml',
    ROOT / 'src/main/resources/META-INF/neoforge.mods.toml',
    ROOT / 'src/main/resources/pack.mcmeta',
):
    if stale_resource.exists():
        fail(f'Stale shared target-specific resource still exists: {stale_resource.relative_to(ROOT)}')

# Project matrix, exact versions and pack metadata.
for node, expected in VERSIONS.items():
    properties_path = ROOT / 'versions' / node / 'gradle.properties'
    if not properties_path.is_file():
        fail(f'Missing version properties: {node}')
        continue
    properties = read_properties(properties_path)
    for key in ('minecraft_version', 'buildcraft_version', 'java_version'):
        if properties.get(key) != expected[key]:
            fail(f'{node}: {key}={properties.get(key)!r}, expected {expected[key]!r}')
    loader_key = 'neo_version' if node.endswith('neoforge') else 'forge_version'
    if properties.get(loader_key) != expected[loader_key]:
        fail(f'{node}: {loader_key}={properties.get(loader_key)!r}, expected {expected[loader_key]!r}')
    if node.endswith('-forge'):
        expected_reobf = 'true' if node in {'1.19.2-forge', '1.20.1-forge'} else 'false'
        if properties.get('forge_reobf') != expected_reobf:
            fail(f'{node}: forge_reobf={properties.get("forge_reobf")!r}, expected {expected_reobf!r}')

    resource_root = ROOT / 'version-resources' / node
    pack_path = resource_root / 'pack.mcmeta'
    if not pack_path.is_file():
        fail(f'Missing pack.mcmeta: {node}')
    else:
        pack = read_json(pack_path).get('pack', {})
        actual_formats = (
            pack.get('pack_format'),
            pack.get('forge:resource_pack_format'),
            pack.get('forge:data_pack_format'),
        )
        if actual_formats != expected['pack']:
            fail(f'{node}: pack formats {actual_formats}, expected {expected["pack"]}')
        if 'supported_formats' in pack:
            fail(f'{node}: unsupported generated supported_formats field remains')

    metadata = 'META-INF/neoforge.mods.toml' if node.endswith('neoforge') else 'META-INF/mods.toml'
    metadata_path = resource_root / metadata
    if not metadata_path.is_file():
        fail(f'Missing loader metadata: {node}/{metadata}')
    else:
        metadata_text = metadata_path.read_text(encoding='utf-8')
        for mod_id in ('buildcraftlib', 'buildcraftcore', 'buildcraftfactory'):
            if f'modId="{mod_id}"' not in metadata_text:
                fail(f'{node}: missing mandatory {mod_id} dependency')

        expanded = metadata_text
        expansion_values = read_properties(ROOT / 'gradle.properties') | properties
        expansion_values['mod_version'] = expansion_values.get('mod_version', '0.0.0') + f'+{expected["minecraft_version"]}'
        for key, value in expansion_values.items():
            expanded = expanded.replace('${' + key + '}', value)
        unresolved = sorted(set(re.findall(r'\$\{([^}]+)\}', expanded)))
        if unresolved:
            fail(f'{node}: unresolved metadata placeholders: {unresolved}')
        else:
            try:
                tomllib.loads(expanded)
            except tomllib.TOMLDecodeError as exc:
                fail(f'{node}: expanded loader metadata is invalid TOML: {exc}')

# Legacy namespace and deleted duplicate GUI must not return.
for relative in STALE_LEGACY_SOURCES:
    if (ROOT / 'src/main/java' / relative).exists():
        fail(f'Stale legacy source still exists on disk: {relative}')
java_paths = sorted((ROOT / 'src/main/java').rglob('*.java'))
java_text = '\n'.join(path.read_text(encoding='utf-8') for path in java_paths)
if len(java_paths) != 13:
    fail(f'Expected 13 Java sources, found {len(java_paths)}')
if 'ct.buildcraft.' in java_text:
    fail('Legacy ct.buildcraft namespace remains in Java sources')
for forbidden in (
    'IronTanksTankMenu', 'IronTanksTankScreen', 'IronTanksRuntimeCompat',
    'IronTanksClientRuntimeCompat', 'java.lang.reflect',
):
    if forbidden in java_text:
        fail(f'Obsolete compatibility/UI code remains referenced: {forbidden}')
for required in (
    'BCCapabilityRegistration.registerBlockEntity',
    'CapUtil.CAP_FLUIDS',
    'new RenderTank(context)',
    'newTank.balanceTankFluids()',
    'FluidAction.SIMULATE',
    'TRANSFER_PER_TICK = 80',
    'BUILDCRAFT_TAB.addItemProvider',
):
    if required not in java_text:
        fail(f'Missing required port behavior: {required}')


# Preserve the original tank specifications and upgrade graph exactly.
blocks_source = (ROOT / 'src/main/java/com/indemnity83/irontanks/common/registry/IronTanksBlocks.java').read_text(encoding='utf-8')
for field, (class_name, capacity, hardness, resistance) in BLOCK_SPECS.items():
    if field == 'CREATIVE_TANK':
        pattern = rf'{field}\s*=\s*BLOCKS\.register\("creative_tank",\s*\(\)\s*->\s*new\s+{class_name}\({capacity}\)\)'
    else:
        pattern = rf'{field}\s*=\s*BLOCKS\.register\("[a-z_]+",\s*\(\)\s*->\s*new\s+{class_name}\({capacity},\s*{re.escape(hardness)},\s*{re.escape(resistance)}\)\)'
    if not re.search(pattern, blocks_source):
        fail(f'Registered tank specification changed or is missing: {field}')

items_source = (ROOT / 'src/main/java/com/indemnity83/irontanks/common/registry/IronTanksItems.java').read_text(encoding='utf-8')
for field, (source, target) in UPGRADE_SPECS.items():
    source_expr = source if source.startswith('BCFactoryBlocks.') else f'IronTanksBlocks.{source}'
    target_expr = f'IronTanksBlocks.{target}'
    pattern = rf'{field}\s*=\s*upgrade\("[a-z_]+",\s*{re.escape(source_expr)},\s*{re.escape(target_expr)}\)'
    if not re.search(pattern, items_source):
        fail(f'Upgrade path changed or is missing: {field} ({source} -> {target})')

# Resolve every Java source for all four nodes and validate target isolation.
for node, expected in VERSIONS.items():
    loader = 'neoforge' if node.endswith('neoforge') else 'forge'
    version = expected['minecraft_version']
    for path in java_paths:
        try:
            rendered = render_stonecutter(path.read_text(encoding='utf-8'), version, loader)
        except ValueError as exc:
            fail(f'{node}:{path.relative_to(ROOT)}: {exc}')
            continue
        if '//?' in rendered:
            fail(f'{node}:{path.relative_to(ROOT)}: unresolved Stonecutter directive')
        if loader == 'forge' and 'net.neoforged.' in rendered:
            fail(f'{node}:{path.relative_to(ROOT)}: NeoForge import leaked into Forge source')
        if loader == 'neoforge' and 'net.minecraftforge.' in rendered:
            fail(f'{node}:{path.relative_to(ROOT)}: Forge import leaked into NeoForge source')
        if version.startswith('1.21'):
            if 'Item.TooltipContext' not in render_stonecutter(
                (ROOT / 'src/main/java/com/indemnity83/irontanks/common/block/TankBlock.java').read_text(encoding='utf-8'),
                version,
                loader,
            ):
                fail(f'{node}: 1.21 tooltip signature was not selected')
            if 'javax.annotation.Nullable' in rendered or 'BlockGetter' in rendered:
                fail(f'{node}:{path.relative_to(ROOT)}: pre-1.21 tooltip import leaked')
        else:
            if 'Item.TooltipContext' in rendered:
                fail(f'{node}:{path.relative_to(ROOT)}: 1.21 tooltip signature leaked')
        structural = strip_java_comments_and_strings(rendered)
        if structural.count('{') != structural.count('}'):
            fail(f'{node}:{path.relative_to(ROOT)}: Java brace count is unbalanced after preprocessing')

# Expected static assets and local model/texture references.
assets = ROOT / 'src/main/resources/assets/irontanks'
blockstates = sorted((assets / 'blockstates').glob('*.json'))
block_models = sorted((assets / 'models/block').glob('*.json'))
item_models = sorted((assets / 'models/item').glob('*.json'))
textures = sorted((assets / 'textures').rglob('*.png'))
if {path.stem for path in blockstates} != set(TANKS):
    fail('Blockstate set does not exactly match the 13 registered tanks')
if len(block_models) != 27:
    fail(f'Expected 27 block models (base + normal/joined variants), found {len(block_models)}')
if {path.stem for path in item_models} != ITEMS:
    fail('Item model set does not exactly match the 27 registered items')
if len(textures) != 52:
    fail(f'Expected 52 PNG textures, found {len(textures)}')
for texture in textures:
    if texture.read_bytes()[:8] != b'\x89PNG\r\n\x1a\n':
        fail(f'Invalid PNG signature: {texture.relative_to(ROOT)}')

for blockstate_path in blockstates:
    blockstate = read_json(blockstate_path)
    variants = blockstate.get('variants', {})
    if set(variants) != {'joined_below=false', 'joined_below=true'}:
        fail(f'{blockstate_path.relative_to(ROOT)}: unexpected joined_below variants')
    for variant in variants.values():
        model_id = variant.get('model', '')
        if model_id.startswith('irontanks:block/'):
            model_path = assets / 'models/block' / f'{model_id.split("/", 1)[1]}.json'
            if not model_path.is_file():
                fail(f'{blockstate_path.relative_to(ROOT)}: missing model {model_id}')

for model_path in block_models + item_models:
    model = read_json(model_path)
    parent = model.get('parent')
    if isinstance(parent, str) and parent.startswith('irontanks:block/'):
        local_parent = assets / 'models/block' / f'{parent.split("/", 1)[1]}.json'
        if not local_parent.is_file():
            fail(f'{model_path.relative_to(ROOT)}: missing local parent {parent}')
    for texture_id in model.get('textures', {}).values():
        if not isinstance(texture_id, str) or texture_id.startswith('#') or not texture_id.startswith('irontanks:'):
            continue
        texture_path = assets / 'textures' / f'{texture_id.split(":", 1)[1]}.png'
        if not texture_path.is_file():
            fail(f'{model_path.relative_to(ROOT)}: missing texture {texture_id}')

# Normal language packs must cover all blocks/items and tooltips.
for language in ('en_us', 'ru_ru', 'zh_cn'):
    lang_path = assets / 'lang' / f'{language}.json'
    lang = read_json(lang_path)
    expected_keys = {f'block.irontanks.{name}' for name in TANKS}
    expected_keys |= {f'item.irontanks.{name}' for name in UPGRADES}
    expected_keys |= {
        'irontanks.tooltip.capacity',
        'irontanks.tooltip.void_tank',
        'irontanks.tooltip.creative_tank',
    }
    missing = expected_keys - set(lang)
    if missing:
        fail(f'{language}: missing language keys: {sorted(missing)}')

# Guide consistency and future external-pack isolation.
guide = assets / 'guide'
if (ROOT / 'src/main/resources/assets/buildcraft').exists():
    fail('Guide integration patches the buildcraft namespace; it must stay external')
manifest = read_json(guide / 'original_manifest.json')
layouts = read_json(guide / 'page_layouts.json')
languages = read_json(guide / 'languages.json')
if (manifest.get('format'), manifest.get('layout_format'), manifest.get('text_pack_format')) != (5, 1, 1):
    fail('Guide manifest format tuple is not 5/1/1')
if layouts.get('format') != 1:
    fail('Guide layout format is not 1')
if languages.get('format') != 1:
    fail('Guide languages format is not 1')
entries = manifest.get('entries', [])
if len(entries) != 27:
    fail(f'Expected 27 guide entries, found {len(entries)}')
ids = [entry.get('id') for entry in entries]
pages_list = [entry.get('page') for entry in entries]
stacks = [entry.get('stack') for entry in entries]
for label, values in (('ids', ids), ('pages', pages_list), ('stacks', stacks)):
    if len(values) != len(set(values)):
        fail(f'Guide entry {label} are not unique')
for entry in entries:
    if entry.get('module') != 'irontanks' or entry.get('book') != 'buildcraftcore:main':
        fail(f'Guide entry has wrong module/book: {entry.get("id")}')
    if entry.get('listed') is not True:
        fail(f'Guide entry is not listed: {entry.get("id")}')
    stack = entry.get('stack', '')
    item_name = stack.split(':', 1)[-1]
    if item_name not in ITEMS:
        fail(f'Guide entry references unknown stack: {stack}')
entry_pages = set(pages_list)
layout_pages = set(layouts.get('pages', {}))
if entry_pages != layout_pages:
    fail(f'Guide manifest/layout page mismatch: missing={sorted(entry_pages-layout_pages)}, extra={sorted(layout_pages-entry_pages)}')
for language in ('en_us', 'ru_ru', 'zh_cn'):
    pack = read_json(guide / 'text' / f'{language}.json')
    if pack.get('format') != 1 or pack.get('language') != language:
        fail(f'Guide text header is invalid for {language}')
    pages = set(pack.get('pages', {}))
    if pages != entry_pages:
        fail(f'Guide text mismatch for {language}: missing={sorted(entry_pages-pages)}, extra={sorted(pages-entry_pages)}')
    for page, values in pack.get('pages', {}).items():
        expected_slots = layouts['pages'][page]['slots']
        if len(values) != expected_slots:
            fail(f'{language}:{page} has {len(values)} text slots, expected {expected_slots}')
registry_lines = [
    line.strip() for line in (guide / 'registry/irontanks.txt').read_text(encoding='utf-8').splitlines()
    if line.strip().startswith(('block_full ', 'item '))
]
if len(registry_lines) != 27:
    fail(f'Guide registry script contains {len(registry_lines)} entries, expected 27')

# Versioned data layout and recipe/loot conventions.
for node in VERSIONS:
    root = ROOT / 'version-resources' / node / 'data'
    modern = node.startswith('1.21.1')
    expected_recipe_dir = root / 'irontanks' / ('recipe' if modern else 'recipes')
    expected_loot_dir = root / 'irontanks' / ('loot_table' if modern else 'loot_tables')
    expected_tag_dir = root / 'minecraft' / 'tags' / ('block' if modern else 'blocks')
    for directory in (expected_recipe_dir, expected_loot_dir, expected_tag_dir):
        if not directory.is_dir():
            fail(f'Missing target data directory: {directory.relative_to(ROOT)}')

    recipes = sorted(expected_recipe_dir.glob('*.json'))
    loot_tables = sorted((expected_loot_dir / 'blocks').glob('*.json'))
    if len(recipes) != 30:
        fail(f'{node}: expected 30 recipes, found {len(recipes)}')
    if {path.stem for path in loot_tables} != set(TANKS):
        fail(f'{node}: loot-table set does not exactly match the 13 tanks')

    for recipe_path in recipes:
        recipe = read_json(recipe_path)
        result = recipe.get('result')
        if not isinstance(result, dict):
            fail(f'{node}: recipe has non-object result: {recipe_path.name}')
            continue
        result_key = 'id' if modern else 'item'
        wrong_key = 'item' if modern else 'id'
        if result_key not in result or wrong_key in result:
            fail(f'{node}: wrong recipe result convention: {recipe_path.name}')
        output_id = result.get(result_key, '')
        if output_id.startswith('irontanks:') and output_id.split(':', 1)[1] not in ITEMS:
            fail(f'{node}: recipe outputs unknown IronTanks item: {recipe_path.name} -> {output_id}')

    for loot_path in loot_tables:
        loot = read_json(loot_path)
        names = []
        for pool in loot.get('pools', []):
            for entry in pool.get('entries', []):
                if entry.get('type') == 'minecraft:item':
                    names.append(entry.get('name'))
        expected_drop = f'irontanks:{loot_path.stem}'
        if expected_drop not in names:
            fail(f'{node}: {loot_path.name} does not drop {expected_drop}')

    pickaxe = read_json(expected_tag_dir / 'mineable/pickaxe.json')
    if set(pickaxe.get('values', [])) != {f'irontanks:{tank}' for tank in TANKS}:
        fail(f'{node}: mineable/pickaxe tag does not contain exactly the 13 tanks')

    all_data_text = '\n'.join(path.read_text(encoding='utf-8') for path in root.rglob('*.json'))
    if node.endswith('neoforge'):
        if '"forge:' in all_data_text:
            fail(f'{node}: NeoForge data still contains a forge: material tag')
        if '"c:' not in all_data_text:
            fail(f'{node}: NeoForge data contains no c: common material tags')
    else:
        if '"c:' in all_data_text:
            fail(f'{node}: Forge data unexpectedly contains c: material tags')

if errors:
    print('IronTanks port verification FAILED:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print('IronTanks port verification passed.')
print(f'JSON files: {len(json_files)}')
print(f'Guide entries: {len(entries)}')
print(f'Java sources: {len(java_paths)}')
print(f'Targets: {len(VERSIONS)}')
print('Resolved Stonecutter source variants: 4')
