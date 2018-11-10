from django.db import models


class Story(models.Model):
    """
    A story that a group of articles refer to or is about.
    """
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.articles.all().first().title
