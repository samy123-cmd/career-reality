from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.backends.signed_cookies import SessionStore
from django.test import RequestFactory, TestCase

from analyzer.salary_access import get_free_previews_remaining


class SalaryAccessReadPathTests(TestCase):
    def test_anonymous_preview_read_does_not_create_session(self):
        """Context-processor reads must not force Set-Cookie on public pages."""
        request = RequestFactory().get("/article/example/")
        request.user = AnonymousUser()
        request.session = SessionStore()

        remaining = get_free_previews_remaining(request)

        self.assertEqual(remaining, 3)
        self.assertFalse(request.session.modified)
        self.assertNotIn("salary_previews_month", request.session)
        self.assertNotIn("salary_previews_used", request.session)
