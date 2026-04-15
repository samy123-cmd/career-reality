from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from companies.models import Company, CompanyReview, Discussion, DiscussionReply


# ─── Helpers ────────────────────────────────────────────────────────────────

def make_company(name="TechCorp", sector="product"):
    return Company.objects.create(name=name, slug=name.lower().replace(" ", "-"), sector=sector)


def make_discussion(company=None, topic="salary", title="Is 20LPA fair at 4 years?", body="Asking for context."):
    return Discussion.objects.create(company=company, topic=topic, title=title, body=body)


# ─── Model Tests ─────────────────────────────────────────────────────────────

class CompanyModelTests(TestCase):
    def test_slug_auto_generated_from_name(self):
        company = make_company("Infosys Ltd")
        self.assertEqual(company.slug, "infosys-ltd")

    def test_slug_not_overwritten_if_set(self):
        company = Company.objects.create(name="Wipro", slug="wipro-custom", sector="service")
        self.assertEqual(company.slug, "wipro-custom")

    def test_str_returns_name(self):
        company = make_company("HCL")
        self.assertEqual(str(company), "HCL")


class DiscussionModelTests(TestCase):
    def test_auto_generates_anonymous_handle(self):
        disc = make_discussion()
        self.assertTrue(disc.anonymous_handle)
        self.assertRegex(disc.anonymous_handle, r"^[A-Za-z]+#\d+$")

    def test_anonymous_handle_is_stable_on_resave(self):
        disc = make_discussion()
        handle = disc.anonymous_handle
        disc.save()
        self.assertEqual(disc.anonymous_handle, handle)

    def test_upvotes_default_zero(self):
        disc = make_discussion()
        self.assertEqual(disc.upvotes, 0)

    def test_discussion_str(self):
        disc = make_discussion(title="Pay transparency at startups")
        self.assertIn("Pay transparency at startups", str(disc))


class DiscussionReplyModelTests(TestCase):
    def test_reply_auto_generates_handle(self):
        disc = make_discussion()
        reply = DiscussionReply.objects.create(discussion=disc, body="Honest answer here.")
        self.assertTrue(reply.anonymous_handle)
        self.assertRegex(reply.anonymous_handle, r"^[A-Za-z]+#\d+$")

    def test_reply_upvotes_default_zero(self):
        disc = make_discussion()
        reply = DiscussionReply.objects.create(discussion=disc, body="My experience.")
        self.assertEqual(reply.upvotes, 0)


# ─── Discussion Views ─────────────────────────────────────────────────────────

class DiscussionListViewTests(TestCase):
    def setUp(self):
        self.company = make_company()
        self.d1 = make_discussion(topic="salary", title="Salary truth")
        self.d2 = make_discussion(company=self.company, topic="culture", title="Culture check")

    def test_list_renders_ok(self):
        response = self.client.get(reverse("discussion_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("page_obj", response.context)

    def test_list_excludes_flagged(self):
        flagged = make_discussion(title="Flagged post")
        flagged.is_flagged = True
        flagged.save()

        response = self.client.get(reverse("discussion_list"))
        titles = [d.title for d in response.context["page_obj"]]
        self.assertNotIn("Flagged post", titles)

    def test_list_filter_by_topic(self):
        response = self.client.get(reverse("discussion_list") + "?topic=salary")
        results = list(response.context["page_obj"])
        self.assertTrue(all(d.topic == "salary" for d in results))

    def test_list_filter_by_company_slug(self):
        response = self.client.get(reverse("discussion_list") + f"?company={self.company.slug}")
        results = list(response.context["page_obj"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].company, self.company)

    def test_list_sort_by_top(self):
        self.d1.upvotes = 10
        self.d1.save()
        response = self.client.get(reverse("discussion_list") + "?sort=top")
        results = list(response.context["page_obj"])
        self.assertEqual(results[0], self.d1)

    def test_total_discussions_in_context(self):
        response = self.client.get(reverse("discussion_list"))
        self.assertIn("total_discussions", response.context)
        self.assertGreaterEqual(response.context["total_discussions"], 2)


class DiscussionDetailViewTests(TestCase):
    def setUp(self):
        self.disc = make_discussion()
        DiscussionReply.objects.create(discussion=self.disc, body="First reply")
        DiscussionReply.objects.create(discussion=self.disc, body="Second reply")

    def test_detail_renders(self):
        response = self.client.get(reverse("discussion_detail", kwargs={"pk": self.disc.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["discussion"], self.disc)

    def test_detail_includes_replies(self):
        response = self.client.get(reverse("discussion_detail", kwargs={"pk": self.disc.pk}))
        self.assertEqual(response.context["reply_count"], 2)

    def test_detail_404_for_flagged_discussion(self):
        self.disc.is_flagged = True
        self.disc.save()
        response = self.client.get(reverse("discussion_detail", kwargs={"pk": self.disc.pk}))
        self.assertEqual(response.status_code, 404)

    def test_detail_excludes_flagged_replies(self):
        flagged = DiscussionReply.objects.create(
            discussion=self.disc, body="Bad reply", is_flagged=True
        )
        response = self.client.get(reverse("discussion_detail", kwargs={"pk": self.disc.pk}))
        reply_bodies = [r.body for r in response.context["replies"]]
        self.assertNotIn("Bad reply", reply_bodies)


class DiscussionCreateViewTests(TestCase):
    _VALID = {
        "topic": "salary",
        "title": "Is 18 LPA fair for 3 years exp?",
        "body": "Looking for real data from people in similar roles.",
        "role": "Backend Engineer",
    }

    def setUp(self):
        cache.clear()

    def test_get_renders_form(self):
        response = self.client.get(reverse("discussion_create"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_valid_post_creates_discussion_and_redirects(self):
        response = self.client.post(reverse("discussion_create"), self._VALID)
        self.assertEqual(Discussion.objects.count(), 1)
        disc = Discussion.objects.first()
        self.assertRedirects(response, reverse("discussion_detail", kwargs={"pk": disc.pk}))

    def test_valid_post_sets_anonymous_handle(self):
        self.client.post(reverse("discussion_create"), self._VALID)
        disc = Discussion.objects.first()
        self.assertTrue(disc.anonymous_handle)

    def test_invalid_post_rerenders_form(self):
        response = self.client.post(reverse("discussion_create"), {"topic": "salary"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Discussion.objects.count(), 0)

    def test_company_discussion_create_links_company(self):
        company = make_company("StartupX")
        response = self.client.post(
            reverse("company_discussion_create", kwargs={"slug": company.slug}),
            self._VALID,
        )
        disc = Discussion.objects.first()
        self.assertIsNotNone(disc)
        self.assertEqual(disc.company, company)

    def test_create_rate_limited(self):
        from django.core.cache import cache
        ip = "127.0.0.1"
        cache.set(f"disc_post_{ip}", 5, 3600)  # already at limit

        response = self.client.post(reverse("discussion_create"), self._VALID, REMOTE_ADDR=ip)
        self.assertEqual(Discussion.objects.count(), 0)
        self.assertRedirects(response, reverse("discussion_list"))

    def test_authenticated_user_attached_to_discussion(self):
        user = User.objects.create_user("authuser", password="pass")
        self.client.login(username="authuser", password="pass")
        self.client.post(reverse("discussion_create"), self._VALID)
        disc = Discussion.objects.first()
        self.assertEqual(disc.user, user)


class DiscussionReplyViewTests(TestCase):
    def setUp(self):
        cache.clear()
        self.disc = make_discussion()

    def test_valid_reply_creates_record(self):
        self.client.post(
            reverse("discussion_reply", kwargs={"pk": self.disc.pk}),
            {"body": "Useful insight from experience."},
        )
        self.assertEqual(DiscussionReply.objects.count(), 1)

    def test_reply_redirects_to_detail(self):
        response = self.client.post(
            reverse("discussion_reply", kwargs={"pk": self.disc.pk}),
            {"body": "My two cents."},
        )
        self.assertRedirects(response, reverse("discussion_detail", kwargs={"pk": self.disc.pk}))

    def test_empty_reply_not_saved(self):
        self.client.post(
            reverse("discussion_reply", kwargs={"pk": self.disc.pk}),
            {"body": ""},
        )
        self.assertEqual(DiscussionReply.objects.count(), 0)

    def test_reply_rate_limited(self):
        from django.core.cache import cache
        ip = "127.0.0.1"
        cache.set(f"disc_reply_{ip}", 5, 3600)

        self.client.post(
            reverse("discussion_reply", kwargs={"pk": self.disc.pk}),
            {"body": "Rate limited response."},
            REMOTE_ADDR=ip,
        )
        self.assertEqual(DiscussionReply.objects.count(), 0)

    def test_reply_to_flagged_discussion_returns_404(self):
        self.disc.is_flagged = True
        self.disc.save()
        response = self.client.post(
            reverse("discussion_reply", kwargs={"pk": self.disc.pk}),
            {"body": "Should not work."},
        )
        self.assertEqual(response.status_code, 404)


class DiscussionUpvoteViewTests(TestCase):
    def setUp(self):
        self.disc = make_discussion()

    def test_upvote_increments_count(self):
        response = self.client.post(reverse("discussion_upvote", kwargs={"pk": self.disc.pk}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["upvotes"], 1)

    def test_upvote_idempotent_within_session(self):
        self.client.post(reverse("discussion_upvote", kwargs={"pk": self.disc.pk}))
        response = self.client.post(reverse("discussion_upvote", kwargs={"pk": self.disc.pk}))
        data = response.json()
        self.assertFalse(data["ok"])
        self.assertEqual(data["error"], "already_voted")
        # DB still has 1 upvote
        self.disc.refresh_from_db()
        self.assertEqual(self.disc.upvotes, 1)

    def test_upvote_flagged_discussion_returns_404(self):
        self.disc.is_flagged = True
        self.disc.save()
        response = self.client.post(reverse("discussion_upvote", kwargs={"pk": self.disc.pk}))
        self.assertEqual(response.status_code, 404)


class CompanyDetailDiscussionTests(TestCase):
    def setUp(self):
        self.company = make_company("FlipKart")
        make_discussion(company=self.company, title="Interview experience at FK")
        make_discussion(company=self.company, title="Culture at FK")

    def test_company_detail_includes_discussions(self):
        response = self.client.get(reverse("company_detail", kwargs={"slug": self.company.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("company_discussions", response.context)

    def test_company_detail_shows_max_5_discussions(self):
        for i in range(6):
            make_discussion(company=self.company, title=f"Post {i}")
        response = self.client.get(reverse("company_detail", kwargs={"slug": self.company.slug}))
        self.assertLessEqual(len(response.context["company_discussions"]), 5)

    def test_company_detail_excludes_flagged_discussions(self):
        flagged = make_discussion(company=self.company, title="Flagged")
        flagged.is_flagged = True
        flagged.save()
        response = self.client.get(reverse("company_detail", kwargs={"slug": self.company.slug}))
        titles = [d.title for d in response.context["company_discussions"]]
        self.assertNotIn("Flagged", titles)
