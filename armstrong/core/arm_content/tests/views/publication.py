from django.core.exceptions import FieldError
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView
from fudge.inspector import arg
from .._utils import *

from ...views import publication


class PublishedModelMixinTestCase(ArmContentTestCase):
    view_class = publication.PublishedModelViewMixin

    def get_view_with_model(self, model):
        view = self.view_class()
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
        qs = fudge.Fake()
        qs.expects("all").returns(qs)
        qs.expects("select_subclasses").returns(expected)
        model = fudge.Fake()
        model.has_attr(published=qs)

        view = self.get_view_with_model(model)
        view.get_queryset()
        fudge.verify()

    def test_can_filter_models_without_published(self):
        qs = fudge.Fake()
        qs.expects("filter").with_args(pub_date__lte=arg.any(),
                pub_status="P")
        model = fudge.Fake()
        model.has_attr(objects=qs)

        view = self.get_view_with_model(model)
        view.get_published_queryset()
        fudge.verify()

    def test_gracefully_handles_models_without_correct_fields(self):
        random_name = "Foo%d" % random.randint(100, 200)
        qs = fudge.Fake()
        qs.expects("filter").raises(FieldError())
        model = fudge.Fake().has_attr(objects=qs, __name__=random_name)
        qs.has_attr(model=model)

        view = self.get_view_with_model(model)
        try:
            view.get_published_queryset()
        except ImproperlyConfigured, e:
            msg = "%s can not be filtered for publication status" % random_name
            self.assertEqual(e.message, msg)


class PublishedModelDetailViewTestCase(PublishedModelMixinTestCase):
    view_class = publication.PublishedModelDetailView


class PublishedModelListViewTestCase(PublishedModelMixinTestCase):
    view_class = publication.PublishedModelListView

    def test_is_mixed_in_with_django_ListView(self):
        self.assertTrue(issubclass(self.view_class, ListView))
