from domain.models import People, Topic
from account.models import Staff

from uuid import uuid1

def randstr():
    return str(uuid1())[0: 10].replace('-', '')


def create_staff(username=None, email=None, password='password', first_name='', last_name='', occupation='', description='', homepage_url=''):

    username = username or randstr()
    email = email or '%s@kmail.com' % username

    staff = Staff.objects.create_user(
        username = username,
        email = email,
        password = password,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url
    )
    staff.save()

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