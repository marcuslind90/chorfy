from django.db import models


class CategoryTag(models.Model):
    """
    Synonyms of a specific category

    E.g. "Business" might be synonym of category "Economy"
    """
    category = models.ForeignKey(
        "core.Category", on_delete=models.CASCADE, related_name="tags"
    )
    name = models.CharField(max_length=50)
