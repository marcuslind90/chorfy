import os
from django.test import TestCase
from unittest.mock import Mock, call, patch
from chorfy.core.models import Article
from .reader import Reader


class ReaderTestCase(TestCase):

    def setUp(self):
        file = open(os.path.dirname(__file__) + "/mocks/rss.xml")
        self.reader = Reader(source=file.read())

    @patch("chorfy.reader.reader.Article.objects.bulk_create")
    def test_save(self, bulk_create):
        """
        Test that save method calls add_article for each entry.
        """
        self.reader.add_article = Mock()
        self.reader.save()

        entry1, entry2, entry3 = self.reader.data.entries
        expected_calls = [
            call(item=entry1), call(item=entry2), call(item=entry3)
        ]
        self.reader.add_article.assert_has_calls(expected_calls)
        bulk_create.assert_called_once()

    def test_add_article(self):
        self.reader.get_keywords = Mock()
        self.reader.get_keywords.return_value = ["mocked", ]
        article = self.reader.add_article(item=self.reader.data.entries[0])
        target = Article(
            title="Dianne Feinstein, Out of Touch? Not Liberal Enough? She Begs to Differ",  # noqa
            summary="Despite murmurs of opposition from her own party, Senator Dianne Feinstein of California is in a dominant position in her campaign for Senate.",  # noqa
            keywords=["mocked", ],
            source="https://www.nytimes.com/2018/11/02/us/dianne-feinstein-senate-california.html?partner=rss&emc=rss"  # noqa
        )

        self.assertEqual(
            [article.title, article.summary, article.keywords, article.source],
            [target.title, target.summary, target.keywords, target.source],
        )

    def test_get_keywords(self):
        """
        Test that expected results are returned from get_keywords
        """
        title = self.reader.data.entries[0].title
        keywords = self.reader.get_keywords(title=title)
        self.assertTrue(
            all(word in keywords for word in [
                "dianne", "feinstein", "liberal", "beg"
            ])
        )

    def test_get_keywords_locations(self):
        """
        Test that Locations are getting included in Keywords.
        """
        title = "Uppsala, Sweden is a beautiful city."
        keywords = self.reader.get_keywords(title=title)
        self.assertTrue(
            all(word in keywords for word in ["uppsala", "sweden", ])
        )

    def test_get_keywords_stemming(self):
        """
        Test that words are getting stemmed in to their base form.
        """
        title = "Kids are going out in the countries"
        keywords = self.reader.get_keywords(title=title)
        self.assertTrue(
            all(word in keywords for word in [
                "countri", "go", "kid",
            ])
        )
