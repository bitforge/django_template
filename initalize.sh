#/bin/bash -e

# Setup environment
ln -sf envs/local.env .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.dev.txt
pip install -r requirements.txt

# Prepare generated django files
./manage.py check
./manage.py makemigrations
./manage.py makemessages -a
./manage.py compilemessages -i .venv

# Remove this file
rm -f $0

# Initialize git repo
git init
git add -A
git commit -m "Initial commit"
git branch -M main
git branch develop
