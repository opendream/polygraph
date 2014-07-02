# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.files import File
from domain.models import People, Topic, PeopleCategory, Statement, Meter
from account.models import Staff
from common.constants import STATUS_DRAFT, STATUS_PENDING, STATUS_PUBLISHED

from uuid import uuid1
import random

def randstr():
    return str(uuid1())[0: 10].replace('-', '')


def create_staff(username=None, email=None, password='password', first_name='', last_name='', occupation='', description='', homepage_url='', image='', is_staff=False):

    username = username or randstr()
    email = email or '%s@kmail.com' % username

    first_name = first_name or randstr()
    last_name = last_name or randstr()
    occupation = occupation or randstr()
    description = description or randstr()
    homepage_url = homepage_url or randstr()
    image = image or '%sdefault/default-people.png' % settings.FILES_WIDGET_TEMP_DIR,


    staff = Staff.objects.create_user(
        username = username,
        email = email,
        password = password,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url,
        image = image
    )

    if is_staff:
        staff.is_staff = True
        staff.save()

    staff = Staff.objects.get(id=staff.id)

    return staff


def create_people_category(permalink=None, title='', description=''):

    permalink = permalink or randstr()
    title = title or randstr()
    description = description or randstr()

    people_category = PeopleCategory.objects.create(
        permalink = permalink,
        title = title,
        description = description
    )

    people_category = PeopleCategory.objects.get(id=people_category.id)

    return people_category


def create_people(permalink=None, first_name='', last_name='', occupation='', description='', homepage_url='', image='', category='', status=STATUS_PUBLISHED, created_by=''):

    created_by = created_by or create_staff()
    permalink = permalink or randstr()
    first_name = first_name or randstr()
    last_name = last_name or randstr()
    occupation = occupation or randstr()
    description = description or randstr()
    homepage_url = homepage_url or randstr()
    image = image or '%sdefault/default-people.png' % settings.FILES_WIDGET_TEMP_DIR,
    category = category or create_people_category()

    people = People.objects.create(
        permalink = permalink,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url,
        image=image,
        status=status,
        created_by=created_by
    )
    people.categories.add(category)
    people.save()

    people = People.objects.get(id=people.id)


    return people


def create_topic(created_by=None, title='', description='', created=None):

    created_by = created_by or create_staff()
    title = title or randstr()
    description = description or randstr()

    topic = Topic.objects.create(
        title  = title,
        description = description,
        created_by = created_by
    )

    topic = Topic.objects.get(id=topic.id)

    return topic


def create_meter(permalink=None, title='', description='', point=0, order=0, image_large_text='', image_medium_text='', image_small_text='', image_small=''):

    permalink = permalink or randstr()
    title = title or randstr()
    description = description or randstr()


    image_large_text = image_large_text or '%sdefault_meters/status-unverifiable---large-text.png' % settings.FILES_WIDGET_TEMP_DIR,
    image_medium_text = image_medium_text or '%sdefault_meters/status-unverifiable---medium-text.png' % settings.FILES_WIDGET_TEMP_DIR,
    image_small_text = image_small_text or '%sdefault_meters/status-unverifiable---small-text.png' % settings.FILES_WIDGET_TEMP_DIR,
    image_small = image_small or '%sdefault_meters/status-unverifiable---small.png' % settings.FILES_WIDGET_TEMP_DIR,



    meter = Meter.objects.create(
        permalink=permalink,
        title=title,
        description=description,
        point=point,
        order=order,
        image_large_text=image_large_text,
        image_small_text=image_small_text,
        image_medium_text=image_medium_text,
        image_small=image_small
    )

    meter = Meter.objects.get(id=meter.id)

    return meter


def create_statement(created_by=None, quoted_by=None, permalink=None, quote='', references=None, status=STATUS_PENDING, topic=None, tags='hello world', meter=None, relate_statements=[], relate_peoples=[], published=None, published_by=None, source=''):

    created_by_list = list(Staff.objects.all()) or [None]
    created_by = created_by or random.choice(created_by_list) or create_staff()

    quoted_by_list = list(People.objects.all()) or [None]
    quoted_by = quoted_by or random.choice(quoted_by_list) or create_people()


    meter_list = list(Meter.objects.all()) or [None]
    meter = meter or random.choice(meter_list) or create_meter()

    topic = topic or create_topic(created_by=created_by)

    permalink = permalink or randstr()

    dummy_text = u'ฮิแฟ็กซ์ อมาตยาธิปไตยอีโรติก สหรัฐแก๊สโซฮอล์ สหรัฐบอเอ็กซ์เพรสคาแร็คเตอร์ชะโป่าไม้สระโงกอ่อนด้อยเทอร์โบบ็อกซ์ ฟลุกแทงโก้สะกอม ฮิแฟ็กซ์ อมาตยาธิปไตยอีโรติก สหรัฐแก๊สโซฮอล์ สหรัฐบอเอ็กซ์เพรสคาแร็คเตอร์ชะโป่าไม้สระโงกอ่อนด้อยเทอร์โบบ็อกซ์ ฟลุกแทงโก้สะกอม ฮิแฟ็กซ์'

    quote = quote or '%s %s' % (dummy_text, randstr())
    source = source or randstr()
    references = references or [{'url': 'http://%s.com/' % randstr(), 'title': randstr()}, {'url': 'http://%s.com/' % randstr(), 'title': randstr()}]
    statement = Statement.objects.create(
        permalink=permalink,
        quote=quote,
        references=references,
        status=status,
        quoted_by=quoted_by,
        created_by=created_by,
        topic=topic,
        tags=tags,
        meter=meter,
        published=published,
        published_by=published_by,
        source=source
    )

    for relate_statement in relate_statements:
        statement.relate_statements.add(relate_statement)

    for relate_people in relate_peoples:
        statement.relate_peoples.add(relate_people)

    statement = Statement.objects.get(id=statement.id)

    return statement