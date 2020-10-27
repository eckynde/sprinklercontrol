"C:\Program Files\PostgreSQL\12\bin\psql.exe" -U postgres -f postgres-setup.sql

py -m pip install --user pipenv
py -m pipenv sync
py -m pipenv shell /C dontrun_setupdjango.bat
