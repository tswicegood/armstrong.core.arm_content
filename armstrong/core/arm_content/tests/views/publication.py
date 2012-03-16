from django.core.exceptions import ImproperlyConfigured
from .._utils import *

from ...views.publication import PublishedModelDetailView


class PublishedModelDetailViewTestCase(ArmContentTestCase):
    def get_view_with_model(self, model):
        view = PublishedModelDetailView()
        view.model = model
        return view

    def test_get_queryset_returns_published_queryset(self):
        expected = random.randint(100, 200)
        qs = fudge.Fake()
        qs.expects("all").returns(expected)
        model = fudge.Fake()
        model.has_attr(published=qs)

        view = self.get_view_with_model(model)
        self.assertEqual(expected, view.get_queryset())
        fudge.verify()

    def test_get_queryset_calls_select_subclasses_if_present(self):
        expected = random.randint(100, 200)
        # other_qs = fudge.Fake()
        # other_qs.expects("select_subclasses").returns(expected)
        qs = fudge.Fake()
        qs.expects("all").returns(qs)
        qs.expects("select_subclasses").returns(expected)
        model = fudge.Fake()
        model.has_attr(published=qs)

        view = self.get_view_with_model(model)
        view.get_queryset()
        fudge.verify()

    def test_gracefully_handles_models_without_published_manager(self):
        class Foo(object):
            pass
        view = self.get_view_with_model(Foo)
        # Use try/catch here for 2.6 compatibility
        try:
            view.get_queryset()
        except ImproperlyConfigured, e:
            self.assertEqual(e.message,
                    "Foo does not have a published property")
