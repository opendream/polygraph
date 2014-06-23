from django.conf import settings
from django.core.files import File
from domain.models import People, Topic, PeopleCategory, Statement, Meter
from account.models import Staff
from common.constants import STATUS_DRAFT, STATUS_PENDING, STATUS_PUBLISHED

from uuid import uuid1

def randstr():
    return str(uuid1())[0: 10].replace('-', '')


def create_staff(username=None, email=None, password='password', first_name='', last_name='', occupation='', description='', homepage_url='', image=''):

    username = username or randstr()
    email = email or '%s@kmail.com' % username

    first_name = first_name or randstr()
    last_name = last_name or randstr()
    occupation = occupation or randstr()
    description = description or randstr()
    homepage_url = homepage_url or randstr()
    image = image or File(open('.%simages/test.jpg' % settings.STATIC_URL), 'test.jpg')


    staff = Staff.objects.create_user(
        username = username,
        email = email,
        password = password,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url,
        image=image
    )

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


def create_people(permalink=None, first_name='', last_name='', occupation='', description='', homepage_url='', image='', category='', status=STATUS_PUBLISHED):

    permalink = permalink or randstr()
    first_name = first_name or randstr()
    last_name = last_name or randstr()
    occupation = occupation or randstr()
    description = description or randstr()
    homepage_url = homepage_url or randstr()
    image = image or File(open('.%simages/test.jpg' % settings.STATIC_URL), 'test.jpg')
    category = category or create_people_category()

    people = People.objects.create(
        permalink = permalink,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url,
        image=image,
        status=status
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


def create_meter(permalink=None, title='', description='', point=0, order=0, image_large_text='', image_small_text='', image_small=''):

    permalink = permalink or randstr()
    title = title or randstr()
    description = description or randstr()


    image_large_text = image_large_text or File(open('.%simages/test.jpg' % settings.STATIC_URL), 'test.jpg')
    image_small_text = image_small_text or File(open('.%simages/test.jpg' % settings.STATIC_URL), 'test.jpg')
    image_small = image_small or File(open('.%simages/test.jpg' % settings.STATIC_URL), 'test.jpg')



    meter = Meter.objects.create(
        permalink=permalink,
        title=title,
        description=description,
        point=point,
        order=order,
        image_large_text=image_large_text,
        image_small_text=image_small_text,
        image_small=image_small
    )

    meter = Meter.objects.get(id=meter.id)

    return meter


def create_statement(created_by=None, quoted_by=None, permalink=None, quote='', references=None, status=STATUS_PUBLISHED, topic=None, tags='hello world', meter=None, relate_statements=[]):

    created_by = created_by or create_staff()
    quoted_by = quoted_by or create_people()
    topic = topic or create_topic(created_by=created_by)
    meter = meter or create_meter()

    permalink = permalink or randstr()
    quote = quote or randstr()
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
        meter=meter
    )

    for relate_statement in relate_statements:
        statement.relate_statements.add(relate_statement)

    statement = Statement.objects.get(id=statement.id)

    return statement