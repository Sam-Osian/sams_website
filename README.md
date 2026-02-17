# Professional website

Source code for https://sam-osian.com.

## Local development

MkDocs (existing site):

```bash
uv run mkdocs serve
```

Django (new site, in parallel):

```bash
uv run python django_site/manage.py migrate
uv run python django_site/manage.py runserver 8010
```
