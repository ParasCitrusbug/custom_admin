import json

from django import template
from django.contrib.admin.utils import quote
from django.utils.safestring import mark_safe

# -----------------------------------------------------------------------------

register = template.Library()


@register.filter
def model_uname(value):
    """Returns a model name such as 'baking_oils'"""
    words = value._meta.verbose_name.lower().replace("&", "").split()
    return "_".join(words)


@register.filter
def model_name(value):
    # return value.__class__.__name__
    return value._meta.verbose_name.title()


@register.filter
def model_name_plural(value):
    return value._meta.verbose_name_plural.title()


@register.filter(is_safe=True)
def as_json(obj):
    return mark_safe(json.dumps(obj))


# -----------------------------------------------------------------------------
# Misc
# -----------------------------------------------------------------------------


@register.filter
def admin_urlname(value, arg):
    if value.model_name == "user":
        pattern = "%s:%s-%s" % ("user", "user", arg)
    if value.model_name == "onboardingquestion":
        pattern = "%s:%s-%s" % ("onboardingquestion", "onboardingquestion", arg)
    if value.model_name == "foodorigin":
        pattern = "%s:%s-%s" % ("foodorigin", "foodorigin", arg)
    if value.model_name == "foodingredient":
        pattern = "%s:%s-%s" % ("foodingredient", "foodingredient", arg)
    if value.model_name == "article":
        pattern = "%s:%s-%s" % ("article", "article", arg)
    else:
        pattern = "%s:%s-%s" % (value.app_label, value.model_name, arg)
    return pattern


@register.filter
def admin_urlquote(value):
    return quote(value)


@register.simple_tag
def field_name(instance, field_name):
    """
    Django template filter which returns the verbose name of an object's,
    model's or related manager's field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()
