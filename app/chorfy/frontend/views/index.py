from django.views.generic import TemplateView
from chorfy.core.models import Story


class Index(TemplateView):
    template_name = "chorfy/frontend/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["stories"] = self.get_stories()
        return context

    def get_stories(self):
        return Story.objects.all().order_by("-pk")
