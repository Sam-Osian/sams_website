from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.test import override_settings


class PageRouteTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Data Scientist at")
        self.assertContains(response, "See CV")
        self.assertContains(response, "Featured post")
        self.assertContains(response, "Contact")

    def test_about_page_renders(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Research that translates into action")
        self.assertContains(response, "See CV")

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

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        CONTACT_EMAIL_RECIPIENT="samoand@liverpool.ac.uk",
        DEFAULT_FROM_EMAIL="website@sam-osian.com",
    )
    def test_contact_form_valid_submission_sends_email(self):
        response = self.client.post(
            reverse("home"),
            {
                "form_name": "contact",
                "name": "Test User",
                "email": "test@example.com",
                "message": "Hello from the contact form",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your message has been sent")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["samoand@liverpool.ac.uk"])
        self.assertIn("Test User", mail.outbox[0].subject)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_contact_form_invalid_submission_shows_errors(self):
        response = self.client.post(
            reverse("home"),
            {
                "form_name": "contact",
                "name": "",
                "email": "not-an-email",
                "message": "",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertEqual(len(mail.outbox), 0)


class PostRouteTests(TestCase):
    def test_published_post_renders(self):
        response = self.client.get(reverse("post-detail", kwargs={"slug": "rethinking-significance"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has the p-value overstayed its welcome")
        self.assertContains(response, "Written by")
        self.assertContains(response, "Tags")
        self.assertContains(response, "Sam Osian")
        self.assertContains(response, 'aria-label="Back to homepage"')

    def test_draft_post_is_hidden(self):
        response = self.client.get(reverse("post-detail", kwargs={"slug": "the-lives-we-could-save"}))
        self.assertEqual(response.status_code, 404)
