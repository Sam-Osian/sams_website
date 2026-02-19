from django.conf import settings
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import redirect, render

from .content import (
    AuthorProfile,
    get_post,
    load_authors_index,
    load_cv,
    load_page,
    load_posts,
    load_posts_config,
    load_site_config,
)
from .forms import ContactForm


def home(request):
    contact_form = ContactForm()
    contact_status = request.session.pop("contact_status", None)

    if contact_status == "validation_error":
        previous_data = request.session.pop("contact_form_data", None)
        if isinstance(previous_data, dict):
            contact_form = ContactForm(previous_data)
            contact_form.is_valid()
        else:
            contact_form = ContactForm()

    if request.method == "POST" and request.POST.get("form_name") == "contact":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data["name"]
            email = contact_form.cleaned_data["email"]
            message = contact_form.cleaned_data["message"]

            email_message = EmailMessage(
                subject=f"New website contact from {name}",
                body=(
                    f"Name: {name}\n"
                    f"Email: {email}\n\n"
                    "Message:\n"
                    f"{message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL_RECIPIENT],
                reply_to=[email],
            )
            try:
                email_message.send(fail_silently=False)
                request.session["contact_status"] = "success"
                response = redirect("home")
                response.status_code = 303
                return response
            except Exception:
                request.session["contact_status"] = "send_error"
                response = redirect("home")
                response.status_code = 303
                return response
        else:
            request.session["contact_status"] = "validation_error"
            request.session["contact_form_data"] = {
                "name": request.POST.get("name", ""),
                "email": request.POST.get("email", ""),
                "message": request.POST.get("message", ""),
            }
            response = redirect("home")
            response.status_code = 303
            return response

    posts = load_posts()
    cv = load_cv()
    site_config = load_site_config()
    posts_config = load_posts_config()

    featured_post_id_raw = posts_config.get("featured_post_id")
    if isinstance(featured_post_id_raw, int):
        featured_post_id = featured_post_id_raw
    elif isinstance(featured_post_id_raw, str):
        try:
            featured_post_id = int(featured_post_id_raw.strip())
        except ValueError:
            featured_post_id = None
    else:
        featured_post_id = None
    featured_post = next((post for post in posts if post.post_id == featured_post_id), None)
    if featured_post is None and posts:
        featured_post = posts[0]

    recent_posts = posts
    if featured_post is not None:
        non_featured_posts = [post for post in posts if post.slug != featured_post.slug]
        recent_posts = non_featured_posts if non_featured_posts else [featured_post]

    return render(
        request,
        "pages/home.html",
        {
            "hero_config": site_config.get("hero", {}),
            "featured_post": featured_post,
            "recent_posts": recent_posts[:3],
            "cv_entries": cv.entries[:4],
            "cv_suggest_prior": len(cv.entries) >= 4,
            "about_preview": str(site_config.get("about_preview", "")).strip(),
            "contact_form": contact_form,
            "contact_status": contact_status,
        },
    )


def about(request):
    site_config = load_site_config()
    cv_content = load_cv()
    return render(
        request,
        "pages/about_showcase.html",
        {
            "about_config": site_config.get("about", {}),
            "cv_entries": cv_content.entries[:3],
            "cv_suggest_prior": len(cv_content.entries) >= 3,
        },
    )


def publications(request):
    page = load_page("publications")
    return render(
        request,
        "pages/page.html",
        {"page": page, "page_key": "publications"},
    )


def cv(request):
    cv_content = load_cv()

    return render(
        request,
        "pages/cv.html",
        {
            "cv": cv_content,
        },
    )


def post_detail(request, slug: str):
    post = get_post(slug=slug)
    if post is None:
        raise Http404("Post not found.")

    authors_index = load_authors_index()
    author_profiles = [authors_index[author] for author in post.authors if author in authors_index]
    missing_authors = [
        author
        for author in post.authors
        if author not in authors_index
    ]
    author_profiles.extend(
        [
            AuthorProfile(
                key=author,
                name=author,
                description="",
                avatar_url=None,
                url=None,
            )
            for author in missing_authors
        ]
    )

    return render(
        request,
        "pages/post_detail.html",
        {"post": post, "author_profiles": author_profiles},
    )
