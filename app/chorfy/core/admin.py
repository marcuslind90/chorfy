from django.contrib import admin
from .models import Article, Story, Publisher, Feed


admin.site.register(Article)
admin.site.register(Feed)
admin.site.register(Publisher)
admin.site.register(Story)
