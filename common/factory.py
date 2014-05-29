from django.conf import settings
from django.core.files import File
from domain.models import People, Topic
from account.models import Staff

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

    #File(open('.%simg/logo.png' % settings.STATIC_URL), 'logo.png')

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
    staff.save()

    staff = Staff.objects.get(id=staff.id)

    return staff


def create_people(permalink=None, first_name='', last_name='', occupation='', description='', homepage_url=''):

    permalink = permalink or randstr()

    people = People.objects.create(
        permalink = permalink,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url
    )
    people = People.objects.get(id=people.id)


    return people


def create_topic(created_by=None, permalink=None, title='', description='', created=None):

    created_by = created_by or create_staff()
    permalink = permalink or randstr()
    title = title or randstr()

    topic = Topic.objects.create(
        permalink = permalink,
        title  = title,
        description = description,
        created_by = created_by
    )

    topic = Topic.objects.get(id=topic.id)

    return topic