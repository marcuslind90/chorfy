import feedparser
import re
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from chorfy.core.models import Article


class Reader(object):
    """
    Read RSS feeds from sources and import the articles.
    """
    def __init__(self, source, *args, **kwargs):
        self.data = feedparser.parse(source)

    def save(self):
        articles = []
        for entry in self.data.entries:
            article = self.add_article(item=entry)
            articles.append(article)

        Article.objects.bulk_create(articles)

    def add_article(self, item):
        article = Article(
            title=item.title,
            summary="".join([content.value for content in item.content]),
            keywords=self.get_keywords(title=item.title),
            source=item.link,
        )
        return article

    def get_keywords(self, title: str):
        stemmer = SnowballStemmer("english")
        stops = set(stopwords.words("english"))

        title = re.sub("[^a-zA-Z0-9 -]+", "", title)
        keywords = title.lower().split(" ")
        keywords = [stemmer.stem(kw) for kw in keywords if kw not in stops]
        return sorted(keywords)
