from datetime import datetime
from model_utils.managers import InheritanceManager


class PublishedManager(InheritanceManager):
    """ Returns published objects where the pub_date has already passed """
    def get_query_set(self):
        return super(PublishedManager, self).get_query_set()\
                .filter(pub_date__lte=datetime.now())\
                .filter(pub_status="P")
