{{ project_name }}
==================

Bitforge Template für neues Django Projekt.

## Template verwenden

Aus diesem Repo kann direkt ein neues Django Projekt erstellt werden:

    git clone git@github.com:bitforge/django_bf_template.git
    django-admin startproject \
        --template django_bf_template \
        --extension py,md \
        project_name

Dannach diese Sektion des READMES entfernen :)


### Setup einmalig

[Postgres.app](https://postgresapp.com) unter MacOS installieren.

Requirements installieren:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # DEV dependencies
    pip install -r requirements.dev.txt

DB einrichten und Admin User erstellen:

    ln -sf envs/local.env .env
    psql -c "create database {{ project_name }}"
    ./manage.py migrate
    ./manage.py createsuperuser


### Konfiguration

Alle variablen Optionen werden gemäss [12factor](https://12factor.net/config) in der Environment definiert.
Im Ordner `envs` können lokal verschiedene Umgebungen erstellt werden werden.
Es gibt jeweils eine aktive Umgebung, die mit dem `.env` Symlink gesetzt wird.
Nach dem auschecken des Repo sollte die lokale PostgreSQL env aktiviert werden.


### Übersetzungen aktualisieren und kompilieren

    ./manage.py makemessages -a
    ./manage.py compilemessages -i .venv


### Dev server starten

Development Server starten

    source .venv/bin/activate
    ./manage.py runserver

