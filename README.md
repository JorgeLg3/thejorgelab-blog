# thejorgelab-blog


# Installation
To run the Django server, first copy the `.example.env` and rename it to `.env`. And then change the values on your interest. The `SECRET_KEY` can be generated with `python -c "import secrets; print(secrets.token_urlsafe())"`

Then you can procede with the `docker compose up --build` to run the server inside a docker container that will serve the app in the port 8000