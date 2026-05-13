# The JorgeLab blog
## Introduction
This is the codebase of my personal blog using Django framework.
- Using UV for project and dependencies management
- The app uses Docker to contain all the code and dependencies
- Github workflows included the build the image and upload it to GH container registry
- Using SQLite in production. SQLite has shown enough performance with the proper settings to be used in production for a lot of use cases
- With the use of bind volumes for the `/media` and `/db-data` you can persist the app data while changing the app code.
- Whitenoise used for manage the staticfiles
- The migrate script is run as part of the Dockerfile entry script. While not ideal, it's safe enough with Django and perfectly valid for my use case. If you prefer to run it separately just remove that part of the `Dockerfile` and use something like: `docker compose run --rm django-app python manage.py migrate --noinput`

## Local development
To run the Django server, first copy the `.example.env` and rename it to `.env`. And then change the values on your interest. The `SECRET_KEY` can be generated with `python3 -c "import secrets; print(secrets.token_urlsafe())"`

Then you can procede with the `docker compose up --build` to run the server inside a docker container that will serve the app in the port 8000 locally

To collect the staticfiles you can use the `uv run manage.py collectstatic`

You can run formatter, linter, type checker and tests with:
```
uv run ruff format
uv run ruff check
uv run ty check
uv run manage.py test
```

## Deployment
The `release.yml` workflow will build and push the docker image to Github container registry. From where you can later consume it. There is an example of docker compose to consume the released image in the `compose-production.yaml`