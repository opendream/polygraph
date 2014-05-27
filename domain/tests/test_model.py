from django.test import TestCase
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from common import factory
from domain.models import Topic


class TestPeople(TestCase):

    def test_create_people(self):

        people1 = factory.create_people('dream.p', 'Dream', 'Politic', 'Prime Minister', 'Black shirt', 'http://dream.politic.com')
        self.assertEqual(people1.first_name, 'Dream')
        self.assertEqual(people1.last_name, 'Politic')
        self.assertEqual(people1.permalink, 'dream.p')
        self.assertEqual(people1.occupation, 'Prime Minister')
        self.assertEqual(people1.description, 'Black shirt')
        self.assertEqual(people1.homepage_url, 'http://dream.politic.com')
        self.assertEqual(people1.get_full_name(), 'Dream Politic')
        self.assertEqual(people1.get_short_name(), 'Dream.P')
        self.assertEqual(people1.__unicode__(), 'dream.p')
        self.assertEqual(people1.inst_name, _('People'))

        people2 = factory.create_people('open.p', 'Open', 'Politic', 'Minister', 'White shirt', 'http://open.politic.com')
        self.assertEqual(people2.first_name, 'Open')
        self.assertEqual(people2.last_name, 'Politic')
        self.assertEqual(people2.permalink, 'open.p')
        self.assertEqual(people2.occupation, 'Minister')
        self.assertEqual(people2.description, 'White shirt')
        self.assertEqual(people2.homepage_url, 'http://open.politic.com')
        self.assertEqual(people2.get_full_name(), 'Open Politic')
        self.assertEqual(people2.get_short_name(), 'Open.P')
        self.assertEqual(people2.__unicode__(), 'open.p')
        self.assertEqual(people2.inst_name, _('People'))


        try:
            with transaction.atomic():
                factory.create_people('dream.p')

            self.assertTrue(0, 'Duplicate permalink allowed.')

        except IntegrityError:
            pass


class TestTopic(TestCase):

    def test_create_topic(self):

        staff1 = factory.create_staff()
        staff2 = factory.create_staff()

        topic1_created1 = timezone.now()
        topic1 = factory.create_topic(staff1, 'hello-world', 'Hello world', 'I am developer', topic1_created1)
        self.assertEqual(topic1.topicrevision_set.count(), 1)
        self.assertEqual(topic1.title, 'Hello world')
        self.assertEqual(topic1.description, 'I am developer')
        self.assertEqual(topic1.created_by, staff1)

        topic1_created2 = timezone.now()
        topic1 = Topic.objects.get(id=topic1.id)
        topic1.title = 'Change title'
        topic1.description = 'Change description'
        topic1.created= topic1_created2
        topic1.created_by = staff2
        topic1.save()

        topic1 = Topic.objects.get(id=topic1.id)

        self.assertEqual(topic1.topicrevision_set.count(), 2)
        self.assertEqual(topic1.title, 'Change title')
        self.assertEqual(topic1.description, 'Change description')
        self.assertEqual(topic1.created_by, staff2)



        topic2 = factory.create_topic(staff2, 'hi-sea', 'Hi sea', 'I am tester')
        self.assertEqual(topic2.topicrevision_set.count(), 1)
        self.assertEqual(topic2.title, 'Hi sea')
        self.assertEqual(topic2.description, 'I am tester')
        self.assertEqual(topic2.created_by, staff2)



        try:
            with transaction.atomic():
                factory.create_topic(staff1, 'hello-world', 'Hello world', 'I am developer')

            self.assertTrue(0, 'Duplicate permalink allowed.')

        except IntegrityError:
            pass

