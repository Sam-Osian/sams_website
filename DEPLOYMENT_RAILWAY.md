# Railway Deployment Notes

## Environment variables

Set these in Railway for your web service:

- `SECRET_KEY` (required, long random string)
- `DEBUG=False`
- `ALLOWED_HOSTS=<your-service>.up.railway.app,sam-osian.com`
- `CSRF_TRUSTED_ORIGINS=https://<your-service>.up.railway.app,https://sam-osian.com`
- `SITE_URL=https://sam-osian.com`
- `DATABASE_URL` (auto-provided when attached to Railway Postgres)

Optional email variables:

- `EMAIL_BACKEND`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `EMAIL_USE_SSL`
- `DEFAULT_FROM_EMAIL`
- `CONTACT_EMAIL_RECIPIENT`

## Build/start commands

- Build command: `uv sync`
- Start command: `python django_site/manage.py migrate && python django_site/manage.py collectstatic --noinput && gunicorn config.wsgi:application --chdir django_site --bind 0.0.0.0:$PORT`
