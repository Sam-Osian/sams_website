from django.http import Http404
from django.shortcuts import render

from .content import get_post, load_cv, load_page, load_posts, load_site_config


def home(request):
    posts = load_posts()
    cv = load_cv()
    site_config = load_site_config()

    featured_post_slug = str(site_config.get("featured_post_slug", "")).strip()
    featured_post = next((post for post in posts if post.slug == featured_post_slug), None)
    if featured_post is None and posts:
        featured_post = posts[0]

    recent_posts = posts
    if featured_post is not None:
        recent_posts = [post for post in posts if post.slug != featured_post.slug]

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
        },
    )


def about(request):
    site_config = load_site_config()
    return render(
        request,
        "pages/about_showcase.html",
        {
            "about_config": site_config.get("about", {}),
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
    return render(request, "pages/post_detail.html", {"post": post})
