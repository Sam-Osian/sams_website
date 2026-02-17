from django.http import Http404
from django.shortcuts import render

from .content import get_post, load_page, load_posts


def home(request):
    page = load_page("home")
    posts = load_posts()
    return render(
        request,
        "pages/home.html",
        {"page": page, "posts": posts},
    )


def about(request):
    page = load_page("about")
    return render(request, "pages/page.html", {"page": page, "page_key": "about"})


def publications(request):
    page = load_page("publications")
    return render(
        request,
        "pages/page.html",
        {"page": page, "page_key": "publications"},
    )


def post_detail(request, slug: str):
    post = get_post(slug=slug)
    if post is None:
        raise Http404("Post not found.")
    return render(request, "pages/post_detail.html", {"post": post})
