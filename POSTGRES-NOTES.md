## PostgreSQL Setup Notes

PostgreSQL version: 12

### Initial setup

CREATE DATABASE sprinklercontrol;
CREATE ROLE sprinklercontrol WITH ENCRYPTED PASSWORD 'sprinkler-password';

### Configuration

ALTER ROLE sprinklercontrol IN DATABASE sprinklercontrol SET client_encoding TO utf8;
ALTER ROLE sprinklercontrol IN DATABASE sprinklercontrol SET default_transaction_isolation TO 'read committed';
ALTER ROLE sprinklercontrol IN DATABASE sprinklercontrol SET timezone TO 'Europe/Berlin';
