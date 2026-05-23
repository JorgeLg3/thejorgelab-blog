import markdown
import bleach

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = {
    "p", "br",
    "h2", "h3",
    "strong", "em", "code", "pre",
    "ul", "ol", "li",
    "blockquote",
    "a",
}

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
}


@register.filter
def markdownify(value):
    html = markdown.markdown(
        value,
        extensions=["extra", "fenced_code"],
    )

    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
    )

    return mark_safe(clean_html)