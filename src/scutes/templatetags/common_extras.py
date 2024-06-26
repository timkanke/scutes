from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def clean_url(context):
    request = context['request']
    return request.build_absolute_uri(request.path)
