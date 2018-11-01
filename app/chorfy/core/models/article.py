from django.contrib.postgres.fields import ArrayField
from django.db import models


class Article(models.Model):
    """
    A News Article from a specific news source.
    """
    story = models.ForeignKey(
        "core.Story", on_delete=models.CASCADE, related_name="articles"
    )
    title = models.CharField(max_length=100)
    summary = models.TextField()
    keywords = ArrayField(models.CharField(max_length=20))
    categories = models.ManyToManyField("core.Category")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
