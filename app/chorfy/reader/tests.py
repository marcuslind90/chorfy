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
        article = self.reader.add_article(item=self.reader.data.entries[0])
        target = Article(
            title="Dianne Feinstein, Out of Touch? Not Liberal Enough? She Begs to Differ",  # noqa
            summary="Despite murmurs of opposition from her own party, Senator Dianne Feinstein of California is in a dominant position in her campaign for Senate.",  # noqa
            keywords=["beg", "diann", "differ", "enough", "feinstein", "liber", "touch", ],  # noqa
            source="https://www.nytimes.com/2018/11/02/us/dianne-feinstein-senate-california.html?partner=rss&emc=rss"  # noqa
        )

        self.assertEqual(
            [article.title, article.summary, article.keywords, article.source],
            [target.title, target.summary, target.keywords, target.source],
        )
