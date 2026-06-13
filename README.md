# FastAPI Payment Test

Async REST API for users, admins, accounts, and payment webhooks.

## Default accounts

User  | `user@test.com`   | `passWorD`   
Admin | `admin@test.com`  | `passWorDadmin`



## Docker

```bash
cp .env.example .env
make up
```

API: http://localhost:8000/docs

## Local

```bash
cp .env.example .env
createdb app
make dev
```

API: http://localhost:8000/docs

## DB setup

Schema and seed data are applied via Alembic only (`alembic/versions/4c60fde4836e_init.py`)
