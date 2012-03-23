from datetime import datetime
from django.db import models
from django.contrib.sites.models import Site


PUB_STATUS_CHOICES = (
    ('D', 'Draft'),
    ('E', 'Edit'),
    ('P', 'Published'),
    ('T', 'Trash'),
)

PUB_STATUSES = dict((pair[1], pair[0]) for pair in PUB_STATUS_CHOICES)


class SimplePublicationMixin(models.Model):
    pub_date = models.DateTimeField(db_index=True)
    pub_status = models.CharField((u'Publication status'), max_length=1,
        choices=PUB_STATUS_CHOICES, help_text=(
            u'Only published items will appear on the site'))

    class Meta:
        abstract = True

    @property
    def is_published(self):
        return (self.pub_date <= datetime.now()
                and self.pub_status == "P")


class PublicationMixin(SimplePublicationMixin, models.Model):
    sites = models.ManyToManyField(Site)

    class Meta:
        abstract = True
