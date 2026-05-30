# The JorgeLab blog
## Introduction
This is the codebase of my personal blog using Django framework.

## Blog Features
- Write posts in Markdown with a server-side preview before publishing
- Tag posts and browse by tag, with a popular-tags sidebar
- Highlight selected posts as "featured"
- Editable About page managed from the admin
- Login-gated authoring (create, edit and delete your own posts) with image uploads

## Framework features
- Using UV for project and dependencies management
- The app uses Docker to contain all the code and dependencies
- GitHub workflows are included to build the image and push it to the GH container registry
- Using SQLite in production. SQLite has shown enough performance with the proper settings to be used in production for a lot of use cases
- With the use of bind volumes for the `/media` and `/db-data` you can persist the app data while changing the app code.
- WhiteNoise used to manage the static files
- The migrate script is run as part of the Dockerfile entry script. While not ideal, it's safe enough with Django and perfectly valid for my use case. If you prefer to run it separately just remove that part of the `Dockerfile` and use something like: `docker compose run --rm django-app python manage.py migrate --noinput`
- Now also incorporates an auth system (only the login view is enabled, since sign-ups are not open to the public)
- Include an Nginx server to handle the user media upload content
- Use markdown and bleach to parse the blog content in Markdown to HTML elements
- Following my minimalist approach to the app dependencies, I'm using no frontend framework and avoiding additional JS wherever possible

## Local development

### Prerequisites
- [Docker](https://www.docker.com/) and Docker Compose
- [UV](https://docs.astral.sh/uv/) and Python 3.14 (only needed to run the host commands below — linting, type-checking, tests)

To run the Django server, first copy the `.example.env` and rename it to `.env`. And then change the values you care about. The `SECRET_KEY` can be generated with `python3 -c "import secrets; print(secrets.token_urlsafe())"`

Then you can proceed with the `docker compose up --build` to run the server inside a docker container that will serve the app in the port 8000 locally. (You can also run the server locally via `uv run manage.py runserver`)

Since sign-ups are closed, create your first user from the running container to log in and author posts:

`docker compose run --rm django-app python manage.py createsuperuser`

To collect the staticfiles you can use the `uv run manage.py collectstatic`

You can run formatter, linter, type checker and tests with:
```
uv run ruff format
uv run ruff check
uv run ty check
uv run manage.py test
```

## Deployment
The `release.yml` workflow will build and push the docker image to Github container registry. From where you can later consume it. You can then create a production compose file with something like this:

```yaml
services:
  django-app:
    image: ghcr.io/jorgelg3/thejorgelab-blog:latest
    restart: unless-stopped
    volumes:
      - ./data/db-data:/app/db-data
      - ./data/media:/app/media
    environment:
      DEBUG: false
      SECRET_KEY: ${SECRET_KEY}
      ALLOWED_HOSTS: ${ALLOWED_HOSTS}
      CSRF_TRUSTED_ORIGINS: ${CSRF_TRUSTED_ORIGINS}

  nginx:
    image: nginx:latest
    restart: unless-stopped
    ports:
      - "8001:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./data/media:/app/media
    depends_on:
      - django-app
```

You will then need to copy the [Nginx config file](nginx.conf) into the root folder from where you are serving the docker compose file.

And finally create a `.env` file next to your compose file to provide the environment variables (`SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`) — see [`.example.env`](.example.env) for reference.