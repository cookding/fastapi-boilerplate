# FastAPI Boilerplate

A template for building server-side applications with FastAPI.

## Development environment

* Python 3.12: to run the app
* PDM: the package and dependency manager
* Docker: to run database setup scripts
* bash: to run some scripts

## How to run for development

```bash
# start database
$ pdm run db-up

# set configurations
$ cp .env.example .env
# edit the variables in `.env` if you want

# restore dependencies
$ pdm install

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
# update the model in code
# update models list in `DataService.models` in `src/app/data/data_service.py`

# generate migration script
$ pdm run migrate-dev-create
# adjust the migration script in `src/app/migrations/models/`
# or
# manually create migration script in `src/app/migrations/models/`

# apply the migration scripts
$ pdm run migrate-deploy
```
