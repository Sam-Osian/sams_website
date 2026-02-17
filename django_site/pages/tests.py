from django.test import TestCase
from django.urls import reverse


class PageRouteTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Data Scientist at")
        self.assertContains(response, "See CV")
        self.assertContains(response, "Featured post")

    def test_about_page_renders(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Research that translates into action")

    def test_publications_page_renders(self):
        response = self.client.get(reverse("publications"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content coming soon")

    def test_cv_page_renders(self):
        response = self.client.get(reverse("cv"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CV")
        self.assertContains(response, "Data Scientist")
        self.assertContains(response, "Back to homepage")


class PostRouteTests(TestCase):
    def test_published_post_renders(self):
        response = self.client.get(reverse("post-detail", kwargs={"slug": "rethinking-significance"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has the p-value overstayed its welcome")

    def test_draft_post_is_hidden(self):
        response = self.client.get(reverse("post-detail", kwargs={"slug": "the-lives-we-could-save"}))
        self.assertEqual(response.status_code, 404)
