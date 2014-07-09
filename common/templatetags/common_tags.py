from django import template
from django.utils import translation
from common.functions import topic_render_reference, image_render
from domain.models import Topic
from common.constants import *


register = template.Library()

@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output  
        return ''


@register.filter(name='topic_render_reference')
def do_topic_render_reference(topic_id):

    topic = Topic.objects.get(id=topic_id)
    return topic_render_reference(topic)


@register.simple_tag(name="image_render")
def do_image_render(image, size, alt='no alt'):

    return image_render(image, size, alt)


@register.filter(name='format_date')
def do_format_date(datetime):

    try:
        lcode = translation.get_language().upper()
        code_month_name = eval('%s_MONTH_NAME' % lcode)
        code_year_plus = eval('%s_YEAR_PLUS' % lcode)

        return unicode('%d %s %d', 'utf-8') % (datetime.day, unicode(code_month_name[datetime.month], 'utf-8'), datetime.year + code_year_plus)

    except:

        return datetime.strftime('%B %d, %Y')


@register.filter(name='format_abbr_date')
def do_format_abbr_date(datetime):

    try:
        lcode = translation.get_language().upper()
        code_month_name = eval('%_MONTH_ABBR_NAME' % lcode)
        code_year_plus = eval('%s_YEAR_PLUS' % lcode)

        return unicode('%d %s %d', 'utf-8') % (datetime.day, unicode(code_month_name[datetime.month], 'utf-8'), (datetime.year + code_year_plus)%100)

    except:
        return datetime.strftime('%b %d, %Y')