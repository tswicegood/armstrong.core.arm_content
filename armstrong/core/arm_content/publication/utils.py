from datetime import datetime


def add_publication_filters(queryset):
    return (queryset.filter(pub_date__lte=datetime.now())
            .filter(pub_status="P"))
