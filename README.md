# FastAPI Boilerplate

A template for building server-side applications with FastAPI.

## Development environment

* Python 3.11: to run the app
* PDM: the package and dependency manager
* Node.js: required by `prisma`
* Docker: to run database setup scripts
* bash: to run some scripts

## How to run for development

```bash
# start database
$ pdm run db-up

# set configurations
$ cp .env.example .env
# edit the variables in `.env` if you want

# restore dependencies & generate prisma client
$ pdm install
$ pdm run prisma-generate

# migrate database
$ pdm run migrate-deploy

# run lint & format
$ pdm run lint

# run tests
$ pdm run test

# run test with coverage
$ pdm run test-cov

# start application
# watch mode
$ pdm run dev
# or
# production mode
$ pdm run start

# stop database
$ pdm run db-down
```

### How to change database schema

```bash
# update schema definitions in prisma/schema.prisma

# format the prisma schema
$ pdm run prisma-format

# generate migration script
$ pdm run migrate-dev-create
# enter the migration script name in the cli interaction

# apply the migration scripts
$ pdm run migrate-deploy

# before start application
# don't forget to generate prisma client based on latest prisma schema
$ pdm run prisma-generate
```
