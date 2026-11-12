#!/bin/bash -e
# Renders this template into a fresh project (like described in README.md)
# and verifies the generated project: system checks, migrations,
# translations and the test suite.
#
# Usage:
#   scripts/test_template.sh
#
# Options via environment:
#   PYTHON=python3.x    Python interpreter used for the test venv (default: python3.14)
#   KEEP=1              Keep the generated project for inspection

TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${PYTHON:-python3.14}"  # Same python version as in alpine:3.24 Docker image
WORK_DIR="$(mktemp -d)"

cleanup() {
  if [ -n "$KEEP" ]; then
    echo "Generated project kept at: $WORK_DIR/testproject"
  else
    rm -rf "$WORK_DIR"
  fi
}
trap cleanup EXIT

echo "==> Creating venv with $($PYTHON --version) in $WORK_DIR"
$PYTHON -m venv "$WORK_DIR/.venv"
. "$WORK_DIR/.venv/bin/activate"
pip install -q --upgrade pip

# Use the psycopg2 binary wheel, so no local libpq / pg_config is required.
# Tests run on sqlite anyway, but this verifies the pinned version resolves.
echo "==> Installing requirements"
sed 's/^psycopg2==/psycopg2-binary==/' "$TEMPLATE_DIR/requirements.txt" > "$WORK_DIR/requirements.txt"
pip install -q -r "$WORK_DIR/requirements.txt" -r "$TEMPLATE_DIR/requirements.dev.txt"

echo "==> Rendering template"
cd "$WORK_DIR"
django-admin startproject \
  --template "$TEMPLATE_DIR" \
  --extension py,md,env,yml \
  testproject
cd testproject

if grep -rn --include='*.py' --include='*.md' --include='*.env' --include='*.yml' '{{ *project_name *}}' .; then
  echo "ERROR: Unrendered template variables found" >&2
  exit 1
fi

echo "==> Running checks"
flake8 src *.py
./manage.py check --fail-level WARNING

echo "==> Creating and applying migrations"
./manage.py makemigrations
./manage.py makemigrations --check --dry-run
./manage.py migrate --verbosity 0

if command -v msgfmt > /dev/null; then
  echo "==> Building translations"
  ./manage.py makemessages -a --verbosity 0
  ./manage.py compilemessages -i .venv --verbosity 0
else
  echo "==> Skipping translations, gettext is not installed"
fi

echo "==> Collecting static files"
./manage.py collectstatic --noinput --verbosity 0

echo "==> Running tests"
./manage.py test src

echo "==> Template OK"
