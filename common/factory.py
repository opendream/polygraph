from django.conf import settings
from django.core.files import File
from domain.models import People, Topic, PeopleCategory
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


def create_people(permalink=None, first_name='', last_name='', occupation='', description='', homepage_url='', image='', category=''):

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
        image=image
    )
    people.categories.add(category)
    people.save()

    people = People.objects.get(id=people.id)


    return people


def create_topic(created_by=None, permalink=None, title='', description='', created=None):

    created_by = created_by or create_staff()
    permalink = permalink or randstr()
    title = title or randstr()
    description = description or randstr()

    topic = Topic.objects.create(
        permalink = permalink,
        title  = title,
        description = description,
        created_by = created_by
    )

    topic = Topic.objects.get(id=topic.id)

    return topic