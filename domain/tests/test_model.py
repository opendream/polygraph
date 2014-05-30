from datetime import timedelta
from django.test import TestCase
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from common import factory
from domain.models import Topic

class TestPeopleCategory(TestCase):

    def test_create_people_category(self):

        people_category1 = factory.create_people_category('politician', 'Politician', 'Politician description bar bar')
        self.assertEqual(people_category1.title, 'Politician')
        self.assertEqual(people_category1.description, 'Politician description bar bar')
        self.assertEqual(people_category1.permalink, 'politician')
        self.assertEqual(people_category1.__unicode__(), 'Politician')

        people_category2 = factory.create_people_category('military', 'Military', 'Military description foo bar')
        self.assertEqual(people_category2.title, 'Military')
        self.assertEqual(people_category2.description, 'Military description foo bar')
        self.assertEqual(people_category2.permalink, 'military')
        self.assertEqual(people_category2.__unicode__(), 'Military')


        try:
            with transaction.atomic():
                factory.create_people_category('politician')

            self.assertTrue(0, 'Duplicate permalink allowed.')

        except IntegrityError:
            pass

class TestPeople(TestCase):

    def setUp(self):

        self.people_category1 = factory.create_people_category('politician', 'Politician')
        self.people_category2 = factory.create_people_category('military', 'Military')


    def test_create_people(self):

        people1 = factory.create_people('dream.p', 'Dream', 'Politic', 'Prime Minister', 'Black shirt', 'http://dream.politic.com', category=self.people_category1)
        self.assertEqual(people1.first_name, 'Dream')
        self.assertEqual(people1.last_name, 'Politic')
        self.assertEqual(people1.permalink, 'dream.p')
        self.assertEqual(people1.occupation, 'Prime Minister')
        self.assertEqual(people1.description, 'Black shirt')
        self.assertEqual(people1.homepage_url, 'http://dream.politic.com')
        self.assertEqual(people1.get_full_name(), 'Dream Politic')
        self.assertEqual(people1.get_short_name(), 'Dream.P')
        self.assertEqual(people1.inst_name, _('People'))
        self.assertEqual(people1.image, 'test.jpg')
        self.assertEqual(list(people1.categories.all()), [self.people_category1])
        self.assertEqual(people1.__unicode__(), 'Dream Politic')

        people2 = factory.create_people('open.p', 'Open', 'Politic', 'Minister', 'White shirt', 'http://open.politic.com', category=self.people_category2)
        self.assertEqual(people2.first_name, 'Open')
        self.assertEqual(people2.last_name, 'Politic')
        self.assertEqual(people2.permalink, 'open.p')
        self.assertEqual(people2.occupation, 'Minister')
        self.assertEqual(people2.description, 'White shirt')
        self.assertEqual(people2.homepage_url, 'http://open.politic.com')
        self.assertEqual(people2.get_full_name(), 'Open Politic')
        self.assertEqual(people2.get_short_name(), 'Open.P')
        self.assertEqual(people2.inst_name, _('People'))
        self.assertEqual(people2.image, 'test.jpg')
        self.assertEqual(list(people2.categories.all()), [self.people_category2])
        self.assertEqual(people2.__unicode__(), 'Open Politic')


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

        # With revision save

        topic1_created1 = timezone.now()
        topic1 = factory.create_topic(staff1, 'hello-world', 'Hello world', 'I am developer', topic1_created1)
        self.assertEqual(topic1.topicrevision_set.count(), 1)
        self.assertEqual(topic1.title, 'Hello world')
        self.assertEqual(topic1.description, 'I am developer')
        self.assertEqual(topic1.created_by, staff1)

        topic1_created2 = timezone.now() - timedelta(days=10)
        topic1_change1 = timezone.now() - timedelta(days=5)
        topic1 = Topic.objects.get(id=topic1.id)
        topic1.title = 'Change title'
        topic1.description = 'Change description'
        topic1.created = topic1_created2
        topic1.changed = topic1_change1
        topic1.created_by = staff2


        self.assertEqual(topic1.topicrevision_set.count(), 1)
        self.assertEqual(topic1.title, 'Change title')
        self.assertEqual(topic1.description, 'Change description')
        self.assertEqual(topic1.created_by, staff2)
        self.assertEqual(topic1.created, topic1_created2)
        self.assertEqual(topic1.changed, topic1_change1)


        topic1.save()

        topic1 = Topic.objects.get(id=topic1.id)

        topic_revision_list = topic1.topicrevision_set.order_by('-id')

        self.assertEqual(topic_revision_list.count(), 2)
        self.assertEqual(topic_revision_list[0].title, 'Change title')
        self.assertEqual(topic_revision_list[1].title, 'Hello world')
        self.assertEqual(topic_revision_list[0].created, topic1_change1)
        self.assertEqual(topic_revision_list[1].created, topic1_created2)
        self.assertEqual(topic1.title, 'Change title')
        self.assertEqual(topic1.description, 'Change description')
        self.assertEqual(topic1.created_by, staff2)
        self.assertEqual(topic1.created, topic1_created2)
        self.assertEqual(topic1.changed, topic1_change1)



        topic2 = factory.create_topic(staff2, 'hi-sea', 'Hi sea', 'I am tester')
        self.assertEqual(topic2.topicrevision_set.count(), 1)
        self.assertEqual(topic2.title, 'Hi sea')
        self.assertEqual(topic2.description, 'I am tester')
        self.assertEqual(topic2.created_by, staff2)


        # Validate
        try:
            with transaction.atomic():
                factory.create_topic(staff1, 'hello-world', 'Hello world', 'I am developer')

            self.assertTrue(0, 'Duplicate permalink allowed.')

        except IntegrityError:
            # check don't create topic
            self.assertEqual(2, Topic.objects.all().count())



        # Without revision save

        topic1.title = 'Change without revision'
        topic1.save(without_revision=True)

        self.assertEqual(topic_revision_list.count(), 2)
        self.assertEqual(topic_revision_list[0].title, 'Change without revision')
        self.assertEqual(topic_revision_list[1].title, 'Hello world')
        self.assertEqual(topic_revision_list[0].created, topic1_change1)
        self.assertEqual(topic_revision_list[1].created, topic1_created2)
        self.assertEqual(topic1.title, 'Change without revision')
        self.assertEqual(topic1.description, 'Change description')
        self.assertEqual(topic1.created_by, staff2)
        self.assertEqual(topic1.created, topic1_created2)
        self.assertEqual(topic1.changed, topic1_change1)





