from datetime import datetime
from model_utils.managers import InheritanceManager

from ..publication.utils import add_publication_filters


class PublishedManager(InheritanceManager):
    """ Returns published objects where the pub_date has already passed """
    def get_query_set(self):
        qs = super(PublishedManager, self).get_query_set()
        return add_publication_filters(qs)
