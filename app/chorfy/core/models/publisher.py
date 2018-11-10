from django.db import models


class Publisher(models.Model):
    """
    A publisher of news and articles.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
