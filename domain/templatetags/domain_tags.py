from django import template
from django.template.loader import render_to_string


register = template.Library()

@register.filter
def statement_item(statement, style='normal'):
    return render_to_string('domain/statement_item_%s.html' % style, {'statement': statement})