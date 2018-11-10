import feedparser
import nltk
from datetime import timedelta
from django.utils.timezone import now
from chorfy.core.models import Article


class Reader(object):
    """
    Read RSS feeds from sources and import the articles.
    """
    def __init__(self, source, *args, **kwargs):
        self.data = feedparser.parse(source)

    def save(self):
        for entry in self.data.entries:
            self.add_article(item=entry)

    def add_article(self, item):
        article = Article.objects.create(
            title=item.title,
            summary="".join([content.value for content in item.content]),
            source=item.link,
        )
        article.tags.add(*self.get_keywords(title=item.title))

        return article

    def get_story(self, article):
        """Get the story of the most similar article

        Similar articles are determined by comparing the tags, and if they
        share more than 1/3 of tags, they're considered similar.

        Arguments:
            article {Article} -- The article we want to find similar story of

        Returns:
            Story -- The story that this article is part of
        """
        # Get similar Articles by tag, sorted by most similar descending.
        similar = article.tags.similar_objects()
        similar = list(filter(
            lambda item: self.filter_similar_articles(
                article=item, compare=article
            ),
            similar
        ))
        if not similar:
            return None
        return similar[0].story

    def filter_similar_articles(self, article: Article, compare: Article):
        limit = article.tags.count()//3
        if article.similar_tags >= limit and \
           article.created_at >= now()-timedelta(days=2):
            return True
        else:
            return False

    def get_keywords(self, title: str):
        """Get keywords from the title

        Use NLTK to determine which words in the title are important
        enough to identify what the story is about and return them
        as asc sorted, lowercase list.

        Arguments:
            title {str} -- The title of the article that we get words from.

        Returns:
            list -- The keywords sorted asc in lowercase.
        """
        # Prepare data
        keywords = set()
        stops = set(nltk.corpus.stopwords.words("english"))
        stemmer = nltk.stem.SnowballStemmer("english")
        ent_types = [
            "PERSON", "ORGANIZATION", "FACILITY", "LOCATION", "DATE",
            "TIME", "GPE", "MONEY",
        ]
        excluded_word_types = ["RB", "IN", "PRP"]

        # Tokenize and chunk words using NLTK
        tokens = nltk.tokenize.word_tokenize(title)
        positions = nltk.pos_tag(tokens)
        chunk = nltk.ne_chunk(positions)

        # Make a word list of keywords we want to add, that
        # are not part of our excluded word types.
        words = set()
        for pos in positions:
            word, word_type = pos
            if word.isalnum() and word_type not in excluded_word_types:
                words.add(word)

        # Add all entities to keyword list and remove them from
        # our remaining word set so they don't get added again
        # and stemmed later.
        for subtree in chunk.subtrees(filter=lambda t: t.label() in ent_types):
            for leaf in subtree.leaves():
                keywords.add(leaf[0])
                words.remove(leaf[0])

        # Add remaining words in list and stem them to base form,
        # stemming means we change words from e.g. "eating" to "eat".
        for word in words:
            if word not in stops:
                keywords.add(stemmer.stem(word))

        return sorted([keyword.lower() for keyword in keywords])
