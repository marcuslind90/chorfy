from django.db import models


class Category(models.Model):
    """
    A topic or category of an article or story.

    E.g "Economy", "Politics" etc.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField()
