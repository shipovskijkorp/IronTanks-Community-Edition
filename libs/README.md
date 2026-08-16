# Local BuildCraft Community Edition jars

BCCE 8.0.14 is not yet published, so ITCE defaults to local BuildCraft dependencies.

Place these files directly in this directory:

- `BuildCraft-Community-Edition-8.0.14+1.19.2+forge.jar`
- `BuildCraft-Community-Edition-8.0.14+1.20.1+forge.jar`
- `BuildCraft-Community-Edition-8.0.14+1.21.1+neoforge.jar`

They are the normal production jars collected by BCCE's corresponding `legacy`/`modern` `buildAndCollect` tasks.

After BCCE 8.0.14 is published, use `-Pbcce_dependency_mode=modrinth` to resolve the matching target from Modrinth Maven instead.
