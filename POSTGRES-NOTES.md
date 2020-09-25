## PostgreSQL Setup Notes

1. PostgreSQL version 12 installieren von Installer, StackBuilder optional
    * [Download](https://www.postgresql.org/download/)
    * User heißt `postgres` mit Passwort aus Installer
    * pgAdmin ist das Webinterface
2. SQL-Skript ausführen
    * ```C:\Program` Files\PostgreSQL\12\bin\psql -U postgres -f postgres-setup.sql```
3. Python-Adapter für Postgres installieren
    * PowerShell öffnen (Virtual environment)
    * `py -m pipenv shell`
    * Python-Adapter für Postgres installieren
    * `pipenv install`
4. Migrate
    * Ggf. PowerShell öffnen (Virtual environment)
    * `py -m pipenv shell`
    * In Ordner 'server' wechseln
    * `cd server`
    * models in der Datenbank anwenden
    * `py manage.py migrate`

### Notiz für Linux

`pg_hba.conf` for connection settings

