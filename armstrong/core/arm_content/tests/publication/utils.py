from django.core.exceptions import FieldError, ImproperlyConfigured
from .._utils import *

from ...publication import utils


class add_publication_filtersTestCase(ArmContentTestCase):
    def test_returns_the_result_of_the_filtered_queryset(self):
        r = random.randint(100, 200)
        qs = fudge.Fake()
        qs.expects("filter").returns(r)
        self.assertEqual(r, utils.add_publication_filters(qs))

    def test_provides_args_for_testing_published_status(self):
        r = random.randint(100, 200)
        datetime = fudge.Fake()
        datetime.expects("now").returns(r)
        qs = fudge.Fake()
        qs.expects("filter").with_args(pub_date__lte=r, pub_status="P")
        with fudge.patched_context(utils, "datetime", datetime):
            utils.add_publication_filters(qs)

    def test_raises_improperly_configured_if_it_cannot_filter(self):
        random_name = "Foo%d" % random.randint(100, 200)
        model = fudge.Fake()
        model.has_attr(__name__=random_name)
        qs = fudge.Fake()
        qs.has_attr(model=model)
        qs.expects("filter").raises(FieldError())

        # Use try/except to keep 2.6 compat
        try:
            utils.add_publication_filters(qs)
        except ImproperlyConfigured, e:
            msg = "%s can not be filtered for publication status" % random_name
            self.assertEqual(e.message, msg)
