from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.fields.related import create_many_related_manager
from django.db.models.fields.related import ManyRelatedObjectsDescriptor


# TODO: find permanent home for this code
def user_to_link(user):
    try:
        return '<a href="%s">%s</a>' % (user.get_profile().get_absolute_url(),
                user.get_full_name())
    except ObjectDoesNotExist:
        return user_to_name(user)


# TODO: find permanent home for this code
def user_to_name(user):
    return user.get_full_name()


class AuthorsManager(User.objects.__class__):
    def has_usable_override(self):
        return hasattr(self.instance, self.override_field_name) and \
                len(getattr(self.instance, self.override_field_name)) > 0

    def has_usable_extra(self):
        return hasattr(self.instance, self.extra_field_name)

    def __unicode__(self, formatter=user_to_name):
        if self.has_usable_override():
            return getattr(self.instance, self.override_field_name)

        names = [formatter(a) for a in self.all()]
        extra = False
        if self.has_usable_extra():
            extra = getattr(self.instance, self.extra_field_name)

        # Warning: weird logic ahead.  It's assumed that ``extra`` has the
        # final conjunction, so we have to join everything by commas.  If
        # there's no ``extra``, we must join the final elements by ``" and "``.
        #
        # TODO: Make this use a template for rendering so its easier to
        # international later on.
        ret = u', '.join(names[:-2] + \
                [(u', ' if extra else u' and ').join(names[-2:])])

        # This adds a space if ``extra`` starts with a letter.  This assumes
        # that anything other than a letter (generally, a comma) should be put
        # directly against the byline.
        if extra:
            space = ' ' if extra[0].isalpha() else ''
            ret = u"%s%s%s" % (ret, space, extra)
        return ret

    def __str__(self):
        return unicode(self)

    def html(self):
        return self.__unicode__(formatter=user_to_link)


class AuthorsDescriptor(object):
    def __init__(self, m2m_field):
        self.field = m2m_field

    def __get__(self, instance, instance_type=None):
        if not instance:
            return self

        RelatedManager = create_many_related_manager(AuthorsManager,
                self.field.rel)
        core_filters = {
            '%s__pk' % self.field.related_query_name(): instance._get_pk_val(),
        }
        manager = RelatedManager(
            model=self.field.rel.to,
            core_filters=core_filters,
            instance=instance,
            symmetrical=self.field.rel.symmetrical,
            source_field_name=self.field.m2m_field_name(),
            target_field_name=self.field.m2m_reverse_field_name(),
            reverse=False,
        )

        # Set this after the fact because AuthorsManager is the superclass and
        # RelatedManager doesn't know about these attributes
        manager.override_field_name = self.field.override_field_name
        manager.extra_field_name = self.field.extra_field_name

        return manager


class AuthorsField(models.ManyToManyField):
    def __init__(self, to=None, override_field_name='authors_override',
            extra_field_name='authors_extra', **kwargs):
        if not to:
            to = User
        self.override_field_name = override_field_name
        self.extra_field_name = extra_field_name
        super(AuthorsField, self).__init__(to=to, **kwargs)

    def contribute_to_class(self, cls, name):
        super(AuthorsField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, AuthorsDescriptor(self))

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "%s.%s" % (self.__class__.__module__,
                self.__class__.__name__)
        args, kwargs = introspector(self)
        kwargs.update({
            'override_field_name': "'%s'" % self.override_field_name,
            'extra_field_name': "'%s'" % self.extra_field_name,
        })
        return (field_class, args, kwargs)
