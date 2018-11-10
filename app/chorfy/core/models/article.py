from django.db import models
from taggit.managers import TaggableManager


class Article(models.Model):
    """
    A News Article from a specific news source.
    """
    story = models.ForeignKey(
        "core.Story",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="articles"
    )
    title = models.CharField(max_length=100)
    summary = models.TextField()
    source = models.URLField()
    categories = models.ManyToManyField("core.Category")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    tags = TaggableManager()
