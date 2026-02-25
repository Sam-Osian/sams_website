from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.core.cache import cache
from django.test import override_settings
import time


class PageRouteTests(TestCase):
    def setUp(self):
        super().setUp()
        cache.clear()

    def _prime_contact_session(self, *, seconds_ago: int = 5):
        self.client.get(reverse("home"))
        session = self.client.session
        session["contact_form_rendered_at"] = int(time.time()) - seconds_ago
        session.save()

    def test_home_page_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Data Scientist at")
        self.assertContains(response, "See CV")
        self.assertContains(response, "Featured post")
        self.assertContains(response, "Contact")
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'class="inline-avatar"', html=False)
        self.assertContains(response, 'src="/static/assets/me-circle-128.webp"', html=False)
        self.assertContains(response, 'alt=""', html=False)

    def test_about_page_renders(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Research that translates into action")
        self.assertContains(response, "See CV")

    def test_publications_page_renders(self):
        response = self.client.get(reverse("publications"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content in preparation")

    def test_cv_page_renders(self):
        response = self.client.get(reverse("cv"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CV")
        self.assertContains(response, "Data Scientist")
        self.assertContains(response, "Back to homepage")

    def test_robots_txt_renders(self):
        response = self.client.get(reverse("robots-txt"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User-agent: *")
        self.assertContains(response, "Sitemap:")

    def test_sitemap_xml_renders(self):
        response = self.client.get(reverse("sitemap-xml"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<urlset", html=False)
        self.assertContains(response, "<loc>", html=False)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        CONTACT_EMAIL_RECIPIENT="samoand@liverpool.ac.uk",
        DEFAULT_FROM_EMAIL="website@sam-osian.com",
    )
    def test_contact_form_valid_submission_sends_email(self):
        self._prime_contact_session(seconds_ago=5)
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
        self._prime_contact_session(seconds_ago=5)
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

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_contact_form_too_fast_submission_is_blocked(self):
        self.client.get(reverse("home"))
        with self.assertLogs("pages.contact_protection", level="WARNING") as logs:
            response = self.client.post(
                reverse("home"),
                {
                    "form_name": "contact",
                    "name": "Fast User",
                    "email": "fast@example.com",
                    "message": "This should be blocked for speed",
                },
                follow=True,
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "delivery issue")
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(any("reason=too_fast" in entry for entry in logs.output))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_contact_form_honeypot_submission_is_ignored(self):
        self._prime_contact_session(seconds_ago=5)
        with self.assertLogs("pages.contact_protection", level="WARNING") as logs:
            response = self.client.post(
                reverse("home"),
                {
                    "form_name": "contact",
                    "name": "Bot User",
                    "email": "bot@example.com",
                    "message": "Spam message",
                    "company_website": "https://spam.example.com",
                },
                follow=True,
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your message has been sent")
        self.assertEqual(len(mail.outbox), 0)
        self.assertTrue(any("reason=honeypot" in entry for entry in logs.output))

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_contact_form_rate_limit_blocks_second_submission_within_minute(self):
        self._prime_contact_session(seconds_ago=5)
        first = self.client.post(
            reverse("home"),
            {
                "form_name": "contact",
                "name": "Normal User",
                "email": "normal@example.com",
                "message": "First message",
            },
            follow=True,
        )
        self.assertEqual(first.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

        self._prime_contact_session(seconds_ago=5)
        with self.assertLogs("pages.contact_protection", level="WARNING") as logs:
            second = self.client.post(
                reverse("home"),
                {
                    "form_name": "contact",
                    "name": "Normal User",
                    "email": "normal@example.com",
                    "message": "Second message",
                },
                follow=True,
            )
        self.assertEqual(second.status_code, 200)
        self.assertContains(second, "delivery issue")
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(any("reason=rate_limit" in entry for entry in logs.output))


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
