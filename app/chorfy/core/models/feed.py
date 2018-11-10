from django.db import models


class Feed(models.Model):
    """
    Synonyms of a specific category

    E.g. "Business" might be synonym of category "Economy"
    """
    publisher = models.ForeignKey(
        "core.Publisher", on_delete=models.CASCADE, related_name="feeds"
    )
    url = models.URLField()

    def __str__(self):
        return self.url
