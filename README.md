New Django App
==============

Bitforge Template für neues Django Projekt.

### Setup einmalig

Postgres.app unter MacOS installieren: https://postgresapp.com/

Requirements installieren:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # DEV dependencies
    pip install -r requirements.dev.txt

DB einrichten und Admin User erstellen:

    ./manage.py migrate
    ./manage.py createsuperuser


### Konfiguration

Alle Config Optionen sollten per Environement Variable definiert werden.
Im Ordner `envs` können verschiedene Umgebungen konfiguriert werden werden.
Es gibt jeweils eine aktive Umgebung, die mit dem `.env` Symlink gesetzt wird.
Nach dem auschecken des Repo sollte die lokale PostgreSQL env aktiviert werden:

    ln -sf envs/local.env .env


### Übersetzungen aktualisieren und kompilieren

    ./manage.py makemessages -a
    ./manage.py compilemessages -i .venv


### Dev server starten

Development Server starten

    source .venv/bin/activate
    ./manage.py runserver 0.0.0.0:8000

