CREATE DATABASE sprinklercontrol;
CREATE ROLE sprinklercontrol WITH ENCRYPTED PASSWORD 'sprinkler-password';
ALTER ROLE sprinklercontrol WITH LOGIN;
GRANT ALL PRIVILEGES ON DATABASE sprinklercontrol TO sprinklercontrol;
ALTER ROLE sprinklercontrol IN DATABASE sprinklercontrol SET client_encoding TO utf8;
ALTER ROLE sprinklercontrol IN DATABASE sprinklercontrol SET default_transaction_isolation TO 'read committed';
ALTER ROLE sprinklercontrol IN DATABASE sprinklercontrol SET timezone TO 'Europe/Berlin';