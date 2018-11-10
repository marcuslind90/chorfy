import feedparser
import nltk
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
            source=item.link,
        )
        return article

    def get_source(self, article):
        pass

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
