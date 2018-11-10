import feedparser
import nltk
from dateutil import parser as dateparser
from datetime import timedelta
from django.utils.timezone import now
from chorfy.core.models import Article, Story


class Reader(object):
    """
    Read RSS feeds from sources and import the articles.
    """
    def __init__(self, source, *args, **kwargs):
        self.data = feedparser.parse(source)

    def save(self):
        for entry in self.data.entries:
            self._add_article(item=entry)

    def _clean_url(self, url):
        """Strips any GET params from url

        Arguments:
            url {str} -- URL we want to strip

        Returns:
            str -- URL stripped of get params
        """
        return "".join(url.split("?")[:1])

    def _add_article(self, item):
        """Take a parser RSS item and adds it as an Article.

        Arguments:
            item {object} -- Item from RSS feed

        Returns:
        """
        # Check if article from this source already exists.
        source = self._clean_url(item.link)
        exists = Article.objects.filter(source=source).count() > 0
        if exists:
            return

        article = Article(
            title=item.title,
            source=source,
            published_at=dateparser.parse(item.published),
        )
        if getattr(item, "content", None):
            article.summary = "".join(
                [content.value for content in item.content]
            )

        article.save()
        article.tags.add(*self._get_keywords(title=item.title))
        article.story = self._get_story(article=article)
        article.save()

        return article

    def _get_story(self, article):
        """Get the story of the most similar article

        Similar articles are determined by comparing the tags, and if they
        share more than 1/3 of tags, they're considered similar.
        If no similar articles are found, create and retunr a new story.

        Arguments:
            article {Article} -- The article we want to find similar story of

        Returns:
            Story -- The story that this article is part of
        """
        # Get similar Articles by tag, sorted by most similar descending.
        similar = article.tags.similar_objects()
        similar = list(filter(
            lambda item: self._filter_similar_articles(
                article=item, compare=article
            ),
            similar
        ))
        if similar:
            return similar[0].story

        # If no similar articles were found, create a new story.
        return Story.objects.create()

    def _filter_similar_articles(self, article: Article, compare: Article):
        """Filter handler to determine if an article is similar or not.

        Arguments:
            article {Article} -- Article we're filtering
            compare {Article} -- Article we are comparing to

        Returns:
            bool -- If article should be filtered out or not.
        """
        limit = article.tags.count()//3
        if article.similar_tags >= limit and \
           article.created_at >= now()-timedelta(days=2):
            return True
        else:
            return False

    def _get_keywords(self, title: str):
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
                if leaf[0] in words:
                    words.remove(leaf[0])

        # Add remaining words in list and stem them to base form,
        # stemming means we change words from e.g. "eating" to "eat".
        for word in words:
            if word not in stops:
                keywords.add(stemmer.stem(word))

        return sorted([keyword.lower() for keyword in keywords])
