from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import DetailView


class PublishedModelDetailView(DetailView):
    def get_queryset(self):
        """
        Returns queryset filtered for only published models

        This makes the assumption that the provided ``model`` attribute
        has a ``published`` property that works as a queryset.  If present,
        it will call ``select_subclasses``.  The ``PublishedManager`` that
        Armstrong provides has a ``select_subclasses`` method.
        """
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
