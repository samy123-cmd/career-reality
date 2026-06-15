from django.test import TestCase
from django.urls import reverse

from ainews.models import AINewsItem
from companies.models import Company
from content.models import Article, Author, Category


class SearchViewTests(TestCase):
    """Tests for the full-text search view and autocomplete API."""

    def setUp(self):
        author = Author.objects.create(
            name="Test Author",
            display_name="Test Author",
            bio="Test bio",
            linkedin_url="https://linkedin.com/in/test",
        )
        category = Category.objects.create(name="Test Category", slug="test-category")
        self.article = Article.objects.create(
            title="Software Engineer Burnout in India",
            slug="software-engineer-burnout",
            author=author,
            category=category,
            status="published",
            actual_reality="Reality text here",
            verdict="Verdict here",
        )
        self.draft_article = Article.objects.create(
            title="Draft Software Engineer Post",
            slug="draft-software-engineer",
            author=author,
            category=category,
            status="draft",
        )
        self.company = Company.objects.create(
            name="Infosys India",
            slug="infosys-india",
        )
        self.news_item = AINewsItem.objects.create(
            title="GPT-5 Impacts Software Jobs",
            slug="gpt-5-impacts-software-jobs",
            summary="A major AI development affecting software engineers.",
            source_name="OpenAI",
            source_url="https://example.com/gpt5",
            status="published",
        )
        self.draft_news = AINewsItem.objects.create(
            title="Draft GPT News",
            slug="draft-gpt-news",
            summary="Draft news item.",
            source_name="Test",
            source_url="https://example.com/draft",
            status="draft",
        )

    def test_search_returns_200(self):
        response = self.client.get(reverse("search"), {"q": "software"})
        self.assertEqual(response.status_code, 200)

    def test_empty_query_returns_200(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)

    def test_search_finds_published_article(self):
        response = self.client.get(reverse("search"), {"q": "software"})
        self.assertIn(self.article, response.context["results"]["articles"])

    def test_search_excludes_draft_article(self):
        response = self.client.get(reverse("search"), {"q": "software"})
        self.assertNotIn(self.draft_article, response.context["results"]["articles"])

    def test_search_finds_company(self):
        self.company.review_count = 1
        self.company.save(update_fields=["review_count"])
        response = self.client.get(reverse("search"), {"q": "infosys"})
        self.assertIn(self.company, response.context["results"]["companies"])

    def test_search_excludes_empty_company(self):
        response = self.client.get(reverse("search"), {"q": "infosys"})
        self.assertNotIn(self.company, response.context["results"]["companies"])

    def test_search_finds_published_ai_news(self):
        response = self.client.get(reverse("search"), {"q": "gpt"})
        self.assertIn(self.news_item, response.context["results"]["news"])

    def test_search_excludes_draft_ai_news(self):
        response = self.client.get(reverse("search"), {"q": "draft"})
        self.assertNotIn(self.draft_news, response.context["results"]["news"])

    def test_short_query_returns_empty_results(self):
        response = self.client.get(reverse("search"), {"q": "a"})
        self.assertEqual(response.context["total"], 0)

    def test_query_truncated_to_max_length(self):
        long_query = "x" * 200
        response = self.client.get(reverse("search"), {"q": long_query})
        self.assertEqual(response.status_code, 200)
        # query in context must be truncated to 100 chars
        self.assertLessEqual(len(response.context["query"]), 100)

    def test_meta_robots_is_noindex(self):
        response = self.client.get(reverse("search"), {"q": "software"})
        self.assertEqual(response.context["meta_robots"], "noindex, follow")


class SearchSuggestApiTests(TestCase):
    """Tests for the JSON autocomplete endpoint."""

    def setUp(self):
        author = Author.objects.create(
            name="API Author",
            display_name="API Author",
            bio="Test bio",
            linkedin_url="https://linkedin.com/in/api-author",
        )
        category = Category.objects.create(name="API Category", slug="api-category")
        self.article = Article.objects.create(
            title="Engineer Career Tips",
            slug="engineer-career-tips",
            author=author,
            category=category,
            status="published",
        )
        self.company = Company.objects.create(name="Wipro Tech", slug="wipro-tech")
        self.news_item = AINewsItem.objects.create(
            title="Engineer Replaced by AI",
            slug="engineer-replaced-by-ai",
            summary="Summary.",
            source_name="TechCrunch",
            source_url="https://example.com/eng",
            status="published",
        )

    def test_suggest_returns_json(self):
        response = self.client.get(reverse("search_suggest"), {"q": "engineer"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_suggest_short_query_returns_empty(self):
        data = self.client.get(reverse("search_suggest"), {"q": "a"}).json()
        self.assertEqual(data["suggestions"], [])

    def test_suggest_finds_article(self):
        data = self.client.get(reverse("search_suggest"), {"q": "engineer"}).json()
        texts = [s["text"] for s in data["suggestions"]]
        self.assertIn("Engineer Career Tips", texts)

    def test_suggest_finds_company(self):
        self.company.review_count = 1
        self.company.save(update_fields=["review_count"])
        data = self.client.get(reverse("search_suggest"), {"q": "wipro"}).json()
        texts = [s["text"] for s in data["suggestions"]]
        self.assertIn("Wipro Tech", texts)

    def test_suggest_excludes_empty_company(self):
        data = self.client.get(reverse("search_suggest"), {"q": "wipro"}).json()
        texts = [s["text"] for s in data["suggestions"]]
        self.assertNotIn("Wipro Tech", texts)

    def test_suggest_finds_ai_news(self):
        data = self.client.get(reverse("search_suggest"), {"q": "engineer"}).json()
        texts = [s["text"] for s in data["suggestions"]]
        self.assertIn("Engineer Replaced by AI", texts)

    def test_suggest_excludes_draft_ai_news(self):
        AINewsItem.objects.create(
            title="Engineer Draft News",
            slug="engineer-draft-news",
            summary="Draft.",
            source_name="Test",
            source_url="https://example.com/d",
            status="draft",
        )
        data = self.client.get(reverse("search_suggest"), {"q": "engineer draft"}).json()
        texts = [s["text"] for s in data["suggestions"]]
        self.assertNotIn("Engineer Draft News", texts)
