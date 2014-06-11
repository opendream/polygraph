from datetime import timedelta
from django.test import TestCase
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from common import factory
from domain.models import Topic, Statement
from common.constants import STATUS_DRAFT, STATUS_PENDING, STATUS_PUBLISHED


class TestPeopleCategory(TestCase):

    def test_create(self):

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


    def test_create(self):

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
        self.assertEqual(people1.status, STATUS_PUBLISHED)
        self.assertEqual(people1.__unicode__(), 'Dream Politic')

        people2 = factory.create_people('open.p', 'Open', 'Politic', 'Minister', 'White shirt', 'http://open.politic.com', category=self.people_category2, status=STATUS_DRAFT)
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
        self.assertEqual(people2.status, STATUS_DRAFT)
        self.assertEqual(people2.__unicode__(), 'Open Politic')


        try:
            with transaction.atomic():
                factory.create_people('dream.p')

            self.assertTrue(0, 'Duplicate permalink allowed.')

        except IntegrityError:
            pass


class TestTopic(TestCase):

    def test_create(self):

        staff1 = factory.create_staff()
        staff2 = factory.create_staff()

        # With revision save

        topic1_created1 = timezone.now()
        topic1 = factory.create_topic(staff1, 'hello-world', 'Hello world', 'I am developer', topic1_created1)
        self.assertEqual(topic1.topicrevision_set.count(), 1)
        self.assertEqual(topic1.title, 'Hello world')
        self.assertEqual(topic1.description, 'I am developer')
        self.assertEqual(topic1.created_by, staff1)
        self.assertEqual(topic1.__unicode__(), 'Hello world')

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
        self.assertEqual(topic1.__unicode__(), 'Change title')



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


class TestStatement(TestCase):

    def setUp(self):

        self.staff1 = factory.create_staff()
        self.staff2 = factory.create_staff()
        self.people1 = factory.create_people()
        self.people2 = factory.create_people()

    def test_create(self):

        statement1 = factory.create_statement(
            created_by=self.staff1,
            quoted_by=self.people1,
            permalink='i-love-polygraph',
            quote='I love polygraph and programming.',
            title='I love polygraph',
            description='I love polygraph and programming. This field is description.',
            references=[{'url': 'http://polygraph.com', 'title': 'Polygraph quote'}, {'url': 'https://google.com', 'title': 'Search yours quotes'}],
            status=STATUS_PUBLISHED
        )
        self.assertEqual(statement1.created_by, self.staff1)
        self.assertEqual(statement1.quoted_by, self.people1)
        self.assertEqual(statement1.permalink, 'i-love-polygraph')
        self.assertEqual(statement1.quote, 'I love polygraph and programming.')
        self.assertEqual(statement1.title, 'I love polygraph')
        self.assertEqual(statement1.description, 'I love polygraph and programming. This field is description.')
        self.assertEqual(statement1.references, [{'url': 'http://polygraph.com', 'title': 'Polygraph quote'}, {'url': 'https://google.com', 'title': 'Search yours quotes'}])
        self.assertEqual(statement1.status, STATUS_PUBLISHED)
        self.assertEqual(statement1.__unicode__(), 'I love polygraph')


        statement2 = Statement.objects.create(
            created_by=self.staff2,
            quoted_by=self.people2,
            permalink='i-love-polygraph-2',
            quote='I love polygraph and programming and testing.',
            title='',
            description='I love polygraph and programming and testing. This field is description.',
            references=[{'url': 'http://polygraph.test', 'title': 'Polygraph test'}, {'url': 'https://test.com', 'title': 'Test your test'}],
            status=STATUS_DRAFT
        )
        self.assertEqual(statement2.created_by, self.staff2)
        self.assertEqual(statement2.quoted_by, self.people2)
        self.assertEqual(statement2.permalink, 'i-love-polygraph-2')
        self.assertEqual(statement2.quote, 'I love polygraph and programming and testing.')
        self.assertEqual(statement2.title, '')
        self.assertEqual(statement2.description, 'I love polygraph and programming and testing. This field is description.')
        self.assertEqual(statement2.references, [{'url': 'http://polygraph.test', 'title': 'Polygraph test'}, {'url': 'https://test.com', 'title': 'Test your test'}])
        self.assertEqual(statement2.status, STATUS_DRAFT)
        self.assertEqual(statement2.__unicode__(), 'I love polygraph and programming and testing.')

        try:
            with transaction.atomic():
                factory.create_statement(permalink='i-love-polygraph')

            self.assertTrue(0, 'Duplicate permalink allowed.')

        except IntegrityError:
            pass



