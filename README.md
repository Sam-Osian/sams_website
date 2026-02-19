# Professional website

Source code for https://sam-osian.com.

## Local development

```bash
uv run python django_site/manage.py migrate
uv run python django_site/manage.py runserver 8010
```

## Content editing

Markdown content now lives in `django_site/content`:

- `django_site/content/index.md`
- `django_site/content/about.md`
- `django_site/content/publications.md`
- `django_site/content/cv.md`
- `django_site/content/posts/*.md`

## Railway deploy (Django)

Use Django as the runtime (no MkDocs build step required).
