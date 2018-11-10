import os
from datetime import timedelta
from django.test import TestCase
from unittest.mock import Mock, call
from chorfy.core.models import Article, Story
from .reader import Reader


class ReaderTestCase(TestCase):

    def setUp(self):
        file = open(os.path.dirname(__file__) + "/mocks/rss.xml")
        self.reader = Reader(source=file.read())

    def test_save(self):
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

    def test_add_article(self):
        article = self.reader.add_article(item=self.reader.data.entries[0])
        target = Article(
            title="Dianne Feinstein, Out of Touch? Not Liberal Enough? She Begs to Differ",  # noqa
            summary="Despite murmurs of opposition from her own party, Senator Dianne Feinstein of California is in a dominant position in her campaign for Senate.",  # noqa
            source="https://www.nytimes.com/2018/11/02/us/dianne-feinstein-senate-california.html?partner=rss&emc=rss"  # noqa
        )

        self.assertEqual(
            [article.title, article.summary, article.source],
            [target.title, target.summary, target.source],
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

    def test_get_story(self):
        story = Story.objects.create()

        # Create base article that we want to find story of.
        foo = Article.objects.create(
            title="foo",
            summary="foo",
            source="http://foo.com",
            story=None,
        )
        foo.tags.add(*["a", "b", "c", "d", ])

        # Create new, partial match article.
        bar = Article.objects.create(
            title="bar",
            summary="bar",
            source="http://bar.com",
            story=story,
        )
        bar.tags.add(*["a", "b", "e", "f", "g", ])

        # Create perfect match article, but old.
        old = Article.objects.create(
            title="old",
            summary="old",
            source="http://old.com",
            story=None,
        )
        old.tags.add(*["a", "b", "c", "d", ])
        old.created_at -= timedelta(days=10)
        old.save()

        res = self.reader.get_story(article=foo)
        self.assertEqual(res, story)
