from datetime import datetime
from django.core.exceptions import FieldError, ImproperlyConfigured


def add_publication_filters(queryset):
    try:
        return queryset.filter(pub_date__lte=datetime.now(),
                pub_status="P")
    except FieldError:
        raise ImproperlyConfigured(
                "%s can not be filtered for publication status" % (
                    queryset.model.__name__))
