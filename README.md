{{ project_name }}
==================

Bitforge Template für neue Django Projekte.

Bringt einige opinionated presets und features mit:

- Docker Container Buildfile
- 12factor env Konfiguration
- Google Cloud Run ready
- Google SSO Login für Admin & Api
- Sentry.io Error Reporting
- Email Addressen als AccountID, keine Usernames
- `django-admin-interface` als Admin Styling
- Django REST Framework für API
- RFC 7807 Error Messages
- SimpleJWT für API Login
- Passwort Reset Flow über API
- `django-imagefields` inkl Admin thumbnails

## Template stanzen

Aus diesem Repo kann direkt ein neues Django Projekt erstellt werden:

    git clone git@github.com:bitforge/django_bf_template.git
    django-admin startproject \
        --template django_bf_template \
        --extension py,md,env \
        project_name


Einmaliges Projekt setup:

    cd project_name

    ln -sf envs/local.env .env
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    ./manage.py check
    ./manage.py makemigrations

    git init
    git commit -a -m "Initial commit"

Dannach diese Sektion des READMES entfernen :)


### Local Dev Setup

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

