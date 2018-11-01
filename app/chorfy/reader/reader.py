import feedparser


class Reader(object):
    """
    Read RSS feeds from sources and import the articles.
    """
    def __init__(self, *args, **kwargs):
        self.parser = feedparser
