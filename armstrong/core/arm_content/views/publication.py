from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import DetailView


class PublishedModelDetailView(DetailView):
    def get_queryset(self):
        try:
            qs = self.model.published.all()
            try:
                return qs.select_subclasses()
            except AttributeError:
                return qs
        except AttributeError:
            raise ImproperlyConfigured(
                "%s does not have a published property" % (
                    self.model.__name__))
