from django.conf import settings


def seo(request):
    site_url = getattr(settings, "SITE_URL", "").strip().rstrip("/")
    if site_url:
        canonical_url = f"{site_url}{request.path}"
        default_image_url = f"{site_url}/static/assets/me-circle.png"
    else:
        canonical_url = request.build_absolute_uri(request.path)
        default_image_url = request.build_absolute_uri("/static/assets/me-circle.png")

    return {
        "seo_site_name": "Sam Osian",
        "seo_default_description": (
            "Sam Osian is a health data scientist and doctoral researcher focused on "
            "AI, open data, and practical tools to improve patient safety."
        ),
        "canonical_url": canonical_url,
        "seo_default_image_url": default_image_url,
    }
