from django.contrib.postgres.fields import ArrayField
from django.db import models


class Story(models.Model):
    """
    A story that articles refer to or is about.
    """
    categories = models.ManyToManyField("core.Category")
    keywords = ArrayField(models.CharField(max_length=20))
    created_at = models.DateTimeField(auto_now_add=True)
