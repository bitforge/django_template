#!/bin/bash -e
cd "$(dirname $0)/.."

echo "Formatting src/ dir with black"

black -S -C \
  --extend-exclude "migrations/*|settings.py" \
  src/