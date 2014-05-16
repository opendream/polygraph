from domain.models import Staff, People

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


def create_people(username=None, first_name='', last_name='', occupation='', description='', homepage_url=''):

    username = username or randstr()

    people = People.objects.create(
        username = username,
        first_name  = first_name,
        last_name = last_name,
        occupation = occupation,
        description = description,
        homepage_url = homepage_url
    )
    people.save()

    return people