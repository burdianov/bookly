```bash

PS C:\Users\Brevis> psql -U postgres
Password for user postgres:
# password: postgres

psql (18.3)
WARNING: Console code page (437) differs from Windows code page (1252)
         8-bit characters might not work correctly. See psql reference
         page "Notes for Windows users" for details.
Type "help" for help.

postgres=# CREATE USER user_name WITH PASSWORD 'password';
CREATE ROLE

postgres=# CREATE DATABASE bookly_db OWNER user_name;
CREATE DATABASE

postgres=# GRANT ALL PRIVILEGES ON DATABASE bookly_db TO user_name;
GRANT
```

```bash
PS C:\Users\Brevis> psql -U user_name -d bookly_db
Password for user user_name:
# password: password
psql (18.3)
```

```bash
# inside psql, connect to bookly_db
\c bookly_db

# view tables
\dt

# describe table 'books'
\d books
```

```bash
alembic init -t async migrations

alembic revision --autogenerate -m "init"

alembic upgrade head
```