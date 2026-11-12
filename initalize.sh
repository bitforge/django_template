#/bin/sh -e

# Setup environment
ln -sf envs/local.env .env
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.dev.txt
pip install -r requirements.txt

# Prepare generated django files
./manage.py check
./manage.py makemigrations
./manage.py makemessages -a
./manage.py compilemessages -i .venv

# Remove this file and the template test
rm -f $0 scripts/test_template.sh

# Initialize git repo
git init
git add -A
git commit -m "Initial commit"
git branch -M main
git branch develop
