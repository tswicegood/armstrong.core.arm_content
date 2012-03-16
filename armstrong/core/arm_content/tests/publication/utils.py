from fudge.inspector import arg
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
