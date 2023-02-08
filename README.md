# Ben İyiyim

[License: Apache Software License 2.0](https://github.com/acikkaynak/ben-iyiyim/blob/main/LICENSE)

## Deployment

The following details how to deploy this application.

## Local Development

```commandline
docker-compose -f local.yml build
docker-compose -f local.yml up
```
* App Url: `http://localhost:8000`
* Documentation Url: `http://localhost:4000`

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.
