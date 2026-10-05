from django import template
from django.utils.html import format_html
from datetime import date, datetime

register = template.Library()


@register.filter
def get_attribute(obj, path):
    if obj is None:
        return None
    for part in path.split('.'):
        if obj is None:
            return None
        obj = getattr(obj, part, None)
    return obj


@register.filter
def render_cell(obj, column):
    attr = column.get('attr', '')
    style = column.get('style', 'text')
    value = get_attribute(obj, attr)

    if callable(value):
        value = value()

    if value is None or value == '':
        return format_html('<span class="text-muted">—</span>')

    if style == 'strong':
        return format_html('<strong>{}</strong>', value)
    if style == 'code':
        return format_html('<code>{}</code>', value)
    if style == 'muted':
        return format_html('<span class="text-muted">{}</span>', value)
    if style == 'date' and isinstance(value, (date, datetime)):
        return value.strftime('%d.%m.%Y')
    if style == 'datetime' and isinstance(value, (date, datetime)):
        return value.strftime('%d.%m.%Y %H:%M')
    if style == 'boolean':
        return 'Да' if value else 'Нет'
    if style == 'medal_badge':
        colors = {'Золото': 'warning', 'Серебро': 'secondary', 'Бронза': 'danger'}
        css = colors.get(str(value), 'secondary')
        return format_html(
            '<span class="badge bg-{} text-dark">{}</span>', css, value
        )
    if style.startswith('badge_'):
        badge_class = style.replace('badge_', '')
        return format_html(
            '<span class="badge bg-{}">{}</span>', badge_class, value
        )

    return value