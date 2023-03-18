# {{ project_name }}

Bitforge Template für neue Django Projekte.

Bringt einige opinionated presets und features mit:

-   [Container build](https://docs.docker.com/engine/reference/builder/) script via `Dockerfile`
-   [12factor](https://12factor.net) Architektur
-   [Google Cloud Run](https://cloud.google.com/run) ready mit [Storage Bucket support.](https://django-storages.readthedocs.io/en/latest/backends/gcloud.html)
-   [Google SSO Login](https://developers.google.com/identity/sign-in/web) **_Deprecated_** für Admin & Api
-   [Sentry.io](https://sentry.io/) Error Reporting
-   Email Addressen als _Account_ID_, keine Usernames
-   [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface) als Admin Styling
-   [Django REST Framework](https://www.django-rest-framework.org/) für API
-   [RFC 7807](https://blog.codecentric.de/2019/09/rest-standardisierte-fehlermeldungen-mittels-rfc-7807-problem-details/) Error Messages
-   [JSON Web Tokens (JWT)](https://jwt.io/) für API Login
-   [django-versatileimagefield](https://django-versatileimagefield.readthedocs.io/en/latest/) für Image Pre-Processing

## Template Take-Off

Aus diesem Repo kann direkt ein neues Django Projekt erstellt werden:

    git clone git@github.com:bitforge/django_template.git

    django-admin startproject \
        --template django_template \
        --extension py,md,env,yml \
        project_name

#### Pre-Flight:

[Postgres.app](https://postgresapp.com) für MacOS installieren, Schritte 1-3 ausführen.

Homebrew installieren: https://brew.sh/

    # Homebrew installieren, falls noch nicht vorhanden
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Python3, gettext und Django installieren
    brew install python@3.10
    brew install gettext
    pip3 install django

#### Cold-Start-Checklist (Git Repo erstellen)

    cd project_name
    ./initalize.sh
    echo "Checklist completed!"

### Test-Flight

Die Triebwerke starten und schauen ob das Ding fliegt:

    source .venv/bin/activate
    echo "Clear!"
    ./manage.py runserver

#### Debriefing & Flight-Log

Repo auf GitHub erstellen und `main` sowie `develop` branch pushen.

Main Branch im Repo auf `develop` setzen.

> Dannach alles in diesem README bis hierhin entfernen & eigenes Intro schreiben.

### Local Dev Setup

#### 1. Postgres Datenbank einrichten

[Postgres.app](https://postgresapp.com) für MacOS installieren, Schritte 1-3 ausführen.

Dannach sollte man sich in der Shell direkt auf die DB connecten können.

    psql

#### 2. Shell Aliases einrichten

Diese Aliases für CLI Commands machen es einfacher, mit Django, Python Envs und Docker zu arbeiten.

Je nach Shell sollten diese in `~/.bashrc` oder `~/.zshrc` gespeichert werden.

    alias cenv='python3 -m venv .venv'
    alias aenv='source .venv/bin/activate'
    alias ienv='pip install -r requirements.txt -r requirements.dev.txt'
    alias fenv='pip freeze -r requirements.txt'
    alias denv='deactivate'

    alias dj='python manage.py'
    alias djr='python manage.py runserver 0.0.0.0:8000'
    alias djmsg='python manage.py makemessages -a -d django'
    alias djmsgc='python manage.py compilemessages -i .venv'

    alias dc='docker-compose'

#### 3. Initial Env Setup

Requirements installieren:

    # Mit Aliases
    cenv
    aenv
    ienv

    # Ohne Aliases
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.dev.txt
    pip install -r requirements.txt

DB einrichten und Admin User erstellen:

    ln -sf envs/local.env .env
    psql -c "create database {{ project_name }}"
    dj migrate
    dj createsuperuser

### Konfiguration

Alle variablen Optionen werden gemäss [12factor](https://12factor.net/config) in der Environment definiert.
Im Ordner `envs` können lokal verschiedene Umgebungen erstellt werden werden.
Es gibt jeweils eine aktive Umgebung, die mit dem `.env` Symlink gesetzt wird.
Nach dem auschecken des Repo sollte die lokale PostgreSQL env aktiviert werden.

### Docker Compose verwenden

Initiales Setup (DB einrichten)

    dc run dj /app/manage.py migrate
    dc run dj /app/manage.py createsuperuser

Dannach kann die Umgebung normal gestartet werden

    dc up

### Übersetzungen aktualisieren und kompilieren

    djmsg
    djmsgc

### Dev server starten

Development Server starten

    aenv
    djr
