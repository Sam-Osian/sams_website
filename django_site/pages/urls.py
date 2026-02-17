from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("publications/", views.publications, name="publications"),
    path("cv/", views.cv, name="cv"),
    path("posts/<slug:slug>/", views.post_detail, name="post-detail-with-prefix"),
    path("<slug:slug>/", views.post_detail, name="post-detail"),
]
