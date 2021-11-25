{{ project_name }}
==================

Bitforge Template für neues Django Projekt.

Bringt einige opinionated presets und features mit:

- [Container build](https://docs.docker.com/engine/reference/builder/) script via `Dockerfile`
- [12factor](https://12factor.net) Architektur
- [Google Cloud Run](https://cloud.google.com/run) ready mit [Storage Bucket support.](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html)
- [Google SSO Login](https://developers.google.com/identity/sign-in/web) für Admin & Api / *Deprecated*
- [Sentry.io](https://sentry.io/) Error Reporting
- Email Addressen als *Account_ID*, keine Usernames
- [`django-admin-interface`](https://github.com/fabiocaccamo/django-admin-interface) als Admin Styling
- [Django REST Framework](https://www.django-rest-framework.org/) für API
- [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) Error Messages
- [JSON Web Tokens (JWT)](https://jwt.io/) für API Login
- [`django-imagefield`](https://github.com/matthiask/django-imagefield) für Image Pre-Processing

## Template stanzen

Aus diesem Repo kann direkt ein neues Django Projekt erstellt werden:

    git clone git@github.com:bitforge/django_bf_template.git
    django-admin startproject \
        --template django_bf_template \
        --extension py,md,env \
        project_name


#### MacOS Setup:

Homebrew installieren: https://brew.sh/

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


#### Linux Setup:

Unter Debian / Ubuntu basierten Distros:

    sudo apt-get install libpq-dev


##### Git & GitHub Repo setup:

    cd project_name
    ./initalize.sh

Repo auf GitHub erstellen und `main` sowie `develop` branch pushen.

Main Branch im Repo auf `develop` setzen.

> Dannach alles in diesem README bis hierhin entfernen & eigenes Intro schreiben.


### Local Dev Setup

[Postgres.app](https://postgresapp.com) unter MacOS installieren.

Requirements installieren:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.dev.txt
    pip install -r requirements.txt

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

