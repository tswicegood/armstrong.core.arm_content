from django.core.exceptions import FieldError, ImproperlyConfigured
from django.views.generic.detail import DetailView

from ..publication.utils import add_publication_filters


class PublishedModelViewMixin(object):
    def get_published_queryset(self):
        try:
            return self.model.published.all()
        except AttributeError:
            try:
                return add_publication_filters(self.model.objects)
            except FieldError:
                raise ImproperlyConfigured(
                        "%s can not be filtered for publication status" % (
                            self.model.__name__))

    def get_queryset(self):
        """
        Returns queryset filtered for only published models

        This makes the assumption that the provided ``model`` attribute
        has a ``published`` property that works as a queryset.  If present,
        it will call ``select_subclasses``.  The ``PublishedManager`` that
        Armstrong provides has a ``select_subclasses`` method.
        """
        qs = self.get_published_queryset()
        try:
            return qs.select_subclasses()
        except AttributeError:
            return qs


class PublishedModelDetailView(PublishedModelViewMixin, DetailView):
    pass
