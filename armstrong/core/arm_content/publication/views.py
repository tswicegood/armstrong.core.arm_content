from django.views.generic import DetailView, ListView
from .utils import add_publication_filters


class PublishedModelViewMixin(object):
    """
    Adjusts view queryset to conform to Armstrong's published concept

    This changes the ``get_queryset`` method to filter out so only published
    data is displayed.  This attempts to use the ``self.model.published``
    manager, but will fall back to manually filtering the queryset as well.

    This assumes that the class' ``model`` property either has a ``published``
    property *or* has a model that has both a ``pub_date`` and ``pub_status``
    field.
    """

    def get_published_queryset(self):
        """
        Returns the raw queryset that is filtered for published status

        This attempts to do the right thing, but will fail by throwing an
        ``ImproperlyConfigured`` exception if the model doesn't contain the
        correct fields.
        """
        try:
            return self.model.published.all()
        except AttributeError:
            return add_publication_filters(self.model.objects)

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
    """Provides a ``DetailView`` that ensures the object is published"""
    pass


class PublishedModelListView(PublishedModelViewMixin, ListView):
    """Provides a ``ListView`` that ensures the objects are published"""
    pass
