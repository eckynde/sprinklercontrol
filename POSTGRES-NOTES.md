## PostgreSQL Setup Notes

1. PostgreSQL version 12 installieren von Installer, StackBuilder optional
    * [Download](https://www.postgresql.org/download/)
    * User heißt `postgres` mit Passwort aus Installer
    * pgAdmin ist das Webinterface
2. SQL-Skript ausführen
    * `psql -U postgres -f postgres.sql`
3. Python-Adapter für Postgres installieren
    * PowerShell öffnen (Virtual environment)
    * `py -m pipenv shell`
    * Python-Adapter für Postgres installieren
    * `pipenv install`
4. Migrate
    * models in der Datenbank anwenden
    * `py manage.py migrate`

### Notiz für Linux

`pg_hba.conf` for connection settings

