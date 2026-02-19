from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class CanonicalHostRedirectMiddleware:
    """Redirect www host to canonical apex host for SEO consistency."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "REDIRECT_WWW_TO_APEX", False):
            canonical_host = getattr(settings, "CANONICAL_HOST", "").strip().lower()
            request_host = request.get_host().split(":", 1)[0].strip().lower()
            www_host = f"www.{canonical_host}" if canonical_host else ""

            if (
                canonical_host
                and request_host == www_host
                and request.method in {"GET", "HEAD"}
            ):
                scheme = "https" if request.is_secure() else "http"
                destination = f"{scheme}://{canonical_host}{request.get_full_path()}"
                return HttpResponsePermanentRedirect(destination)

        return self.get_response(request)
