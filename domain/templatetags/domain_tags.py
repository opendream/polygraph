from django import template
from django.template.loader import render_to_string


register = template.Library()

@register.filter
def statement_item(statement, style='normal'):
    return render_to_string('domain/statement_item_%s.html' % style, {'statement': statement})

@register.filter
def meter_count(meter_statement_count):

    total = 0
    for meter, count in meter_statement_count:
        if count > total:
            total = count

    meter_statement_count_percent = []
    for meter, count in meter_statement_count:
        if total == 0:
            percent = 100
        else:
            percent = count*100/total
        meter_statement_count_percent.append((meter, count, percent))


    return render_to_string('domain/meter_count.html', {
        'meter_statement_count': meter_statement_count_percent
    })

