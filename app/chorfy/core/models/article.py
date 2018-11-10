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
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    source = models.URLField()
    categories = models.ManyToManyField("core.Category")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    tags = TaggableManager()

    def __str__(self):
        return self.title
