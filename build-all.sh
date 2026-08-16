#!/usr/bin/env bash
set -Eeuo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
if (( $# == 0 )); then
  gradle_args=(buildAndCollect)
else
  gradle_args=("$@")
fi

for generation in legacy modern; do
  echo "==> Running ${generation} Iron Tanks build: ${gradle_args[*]}"
  (
    cd "${repo_root}/builds/${generation}"
    exec ./gradlew "${gradle_args[@]}"
  )
done
