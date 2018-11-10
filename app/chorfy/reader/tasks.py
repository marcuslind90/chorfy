from chorfy.core.models import Publisher
from .reader import Reader


def import_feeds():
    publishers = Publisher.objects.all()
    for publisher in publishers:
        for feed in publisher.feeds.all():
            reader = Reader(feed.url)
            reader.save()
