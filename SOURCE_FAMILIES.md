# Iron Tanks build generations and source layout

Iron Tanks Community Edition follows the same multi-generation layout used by BuildCraft Community Edition. The repository has two independent Gradle/Stonecutter builds and one layered source tree.

## Build generations

### `legacy`

Targets:

- `1.19.2-forge`
- `1.20.1-forge`

Build root: `builds/legacy`

This generation owns the ForgeGradle targets and has its own Gradle wrapper and Stonecutter controller.

### `modern`

Targets:

- `1.21.1-neoforge`

Build root: `builds/modern`

The modern wrapper is independent so future NeoForge/Fabric ports can upgrade Gradle, Stonecutter or Java without forcing those requirements onto the legacy Forge build.

## Repository layout

```text
build-config/
├─ common.properties
└─ generations.properties

builds/
├─ legacy/
└─ modern/

source-shared/
└─ src/                         code/resources valid everywhere

source-families/
├─ legacy/                      Minecraft-generation implementation
└─ modern/

source-platforms/
├─ forge/                       Forge registration/capability glue
└─ neoforge/                    NeoForge registration/capability glue

version-src/
├─ 1.19.2-forge/
├─ 1.20.1-forge/
└─ 1.21.1-neoforge/             target-only metadata and resources
```

Each target is materialized as:

```text
shared + family + platform + target overlay = effective target source tree
```

Later layers override the same logical path from earlier layers. The generated tree lives under the target build directory and is never authoritative source.

## Placement rules

- Put common gameplay, API2 integration, models, recipes and textures in `source-shared`.
- Put broad Minecraft-generation differences in `source-families/<generation>`.
- Put loader imports, event buses, registries, capabilities and loader lifecycle code in `source-platforms/<loader>`.
- Put only irreducible target-specific files in `version-src/<target>`; currently this is loader metadata and `pack.mcmeta`.
- Do not reintroduce full per-version source copies.

The 1.19.2 implementation remains the behaviour reference. Source code may differ across generations/loaders, but player-visible Iron Tanks behaviour should remain equivalent.

## Build commands

Build every generation:

```bash
./build-all.sh
```

Windows PowerShell:

```powershell
./build-all.ps1
```

Build only one generation:

```bash
cd builds/legacy
./gradlew buildAndCollect
```

```bash
cd builds/modern
./gradlew buildAndCollect
```

Run the active target:

```bash
cd builds/legacy
./gradlew runActiveClient
```

```bash
cd builds/modern
./gradlew runActiveClient
```

List targets and validate the architecture:

```bash
python scripts/validate-stonecutter.py --list-targets
python scripts/validate-stonecutter.py
python scripts/validate-source-families.py
python scripts/verify_port.py
```

## BuildCraft dependency

BCCE 8.0.14 is unreleased, so local jars are the default. Put the matching jars in `libs/` using the names documented in `libs/README.md`.

When matching BCCE artifacts are published, a build can be switched explicitly with:

```bash
./gradlew buildAndCollect -Pbcce_dependency_mode=modrinth
```
