from django.core.urlresolvers import reverse
from django.http import Http404, HttpRequest
from django.utils.translation import ugettext_lazy as _

from django.test import TestCase

from common import factory
from domain.models import People, Topic, Statement
from common.constants import STATUS_DRAFT, STATUS_PENDING, STATUS_PUBLISHED
from domain.views import domain_delete


class TestDeleteDomain(TestCase):

    def setUp(self):

        if not hasattr(self, 'inst_name'):
            return

        self.query = eval(self.inst_name.title()).objects.all()
        self.created_by = factory.create_staff()
        self.inst = getattr(factory, 'create_%s' % self.inst_name)(created_by=self.created_by)
        self.url = reverse('domain_delete', args=[self.inst_name, self.inst.id])

    def test_delete_success(self):

        if not hasattr(self, 'inst_name'):
            return

        self.client.login(username=self.created_by.username, password='password')
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(0, self.query.filter(id=self.inst.id).count())
        self.assertContains(response, _('Your %s has been deleted.') % self.inst_name)

    def test_delete_authorize(self):

        if not hasattr(self, 'inst_name'):
            return

        # not login
        response = self.client.get(self.url)
        self.assertRedirects(response, '%s?next=%s' % (reverse('account_login'), self.url))

        # login and not inst owner
        other_staff = factory.create_staff()
        self.client.login(username=other_staff.username, password='password')
        #response = self.client.get(self.url)
        request = HttpRequest()
        request.user = other_staff
        self.assertRaises(Http404, domain_delete, request, 'people', self.inst.id)

        self.client.logout()

        # login and staff permission
        staff = factory.create_staff(is_staff=True)
        self.client.login(username=staff.username, password='password')
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(0, self.query.filter(id=self.inst.id).count())


class TestEditPeople(TestCase):

    def setUp(self):

        self.people_category1 = factory.create_people_category('politician', 'Politician')
        self.people_category2 = factory.create_people_category('military', 'Military')

        self.staff1 = factory.create_staff('staff', 'crosalot@kmail.com', 'password', ' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.people2 = factory.create_people('panudate',' Panudate', 'Vasinwattana', 'Tester', 'Unittest', 'http://opendream.in.th', category=self.people_category1)

        self.client.login(username=self.staff1.username, password='password')

        # Define for override
        self.check_initial = True
        self.people1 = factory.create_people('crosalot',' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th', category=self.people_category2, status=STATUS_DRAFT)
        self.url1 = reverse('people_edit', args=[self.people1.id])
        self.url2 = reverse('people_edit', args=[self.people2.id])
        self.message_success = _('Your %s settings has been updated. View this %s <a href="%s">here</a>.') % (_('people'), _('people'), '#')
        self.title = _('Edit %s') % _('People')
        self.button = _('Save changes')



    def test_get_edit_page(self):

        self.client.logout()

        response = self.client.get(self.url1)
        self.assertRedirects(response, '%s?next=%s' % (reverse('account_login'), self.url1))

        self.client.login(username=self.staff1.username, password='password')
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'domain/people_form.html')
        self.client.logout()

    def test_edit_context(self):
        response = self.client.get(self.url1)

        self.assertContains(response, 'name="permalink"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="occupation"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'name="homepage_url"')
        self.assertContains(response, 'name="image"')
        self.assertContains(response, 'name="categories"')
        self.assertContains(response, 'name="status"')
        self.assertContains(response, self.title)
        self.assertContains(response, self.button)

        if not self.check_initial:
            return

        self.assertContains(response, self.people1.permalink)
        self.assertContains(response, self.people1.first_name)
        self.assertContains(response, self.people1.last_name)
        self.assertContains(response, self.people1.occupation)
        self.assertContains(response, self.people1.description)
        self.assertContains(response, self.people1.homepage_url)



        response = self.client.get(self.url2)
        self.assertContains(response, self.people2.permalink)
        self.assertContains(response, self.people2.first_name)
        self.assertContains(response, self.people2.last_name)
        self.assertContains(response, self.people2.occupation)
        self.assertContains(response, self.people2.description)
        self.assertContains(response, self.people2.homepage_url)

    def test_edit_post(self):

        params = {
            'permalink': self.people1.permalink,
            'first_name': self.people1.first_name,
            'last_name': self.people1.last_name,
            'occupation': self.people1.occupation,
            'description': self.people1.description,
            'homepage_url': self.people1.homepage_url,
            'categories': [self.people_category1.id],
            'status': self.people1.status,
        }

        response = self.client.post(self.url1, params, follow=True)

        if self.people1.id:
            self.people1 = People.objects.get(id=self.people1.id)
        else:
            self.people1 = People.objects.latest('id')


        self.assertContains(response, self.people1.permalink)
        self.assertContains(response, self.people1.first_name)
        self.assertContains(response, self.people1.last_name)
        self.assertContains(response, self.people1.occupation)
        self.assertContains(response, self.people1.description)
        self.assertContains(response, self.people1.homepage_url)
        self.assertContains(response, self.message_success)

        self.assertEqual(list(response.context['form'].initial['categories']), [self.people_category1])
        self.assertEqual(response.context['form'].initial['status'], self.people1.status)



    def test_has_new(self):
        before = People.objects.all().count()
        self.test_edit_post()
        after = People.objects.all().count()

        self.assertEqual(int(not self.check_initial), after-before)


    def test_post_edit_invalid(self):

        params = {
            'permalink': '',
            'first_name': '',
            'last_name': '',
            'occupation': '',
            'description': '',
            'homepage_url': '',
            'categories': [],
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink', [_('This field is required.')])
        self.assertFormError(response, 'form', 'first_name', [_('This field is required.')])
        self.assertFormError(response, 'form', 'last_name', [_('This field is required.')])
        self.assertFormError(response, 'form', 'categories', [_('This field is required.')])


        params = {
            'permalink': self.people2.permalink,
            'first_name': self.people1.first_name,
            'last_name': self.people1.last_name,
            'occupation': '',
            'description': '',
            'homepage_url': '',
            'categories': [],
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink',  [_('This permalink is already in use.')])


        params = {
            'permalink': 'a tom in link?',
            'first_name': self.people1.first_name,
            'last_name': self.people1.last_name,
            'occupation': '',
            'description': '',
            'homepage_url': '',
            'categories': [],
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink',  [_('Enter a valid permalink.')])

        self.client.logout()

    def test_post_edit_not_update(self):

        params = {
            'permalink': self.people1.permalink,
            'first_name': self.people1.first_name,
            'last_name': self.people1.last_name,
            'categories': [self.people_category1.id],

        }

        response = self.client.post(self.url1, params, follow=True)
        self.assertContains(response, self.message_success)


class TestCreatePeople(TestEditPeople):

    def setUp(self):
        super(TestCreatePeople, self).setUp()

        self.check_initial = False

        self.people1 = People(**{
            'permalink': 'new-crosalot',
            'first_name': 'New',
            'last_name': 'Crosalot',
            'occupation': 'Designer',
            'description': 'Work on opendream',
            'homepage_url': 'http://opendream.co.th',
            'status': STATUS_DRAFT,
        })
        self.url1 = reverse('people_create')
        self.url2 = reverse('people_create')
        self.message_success = _('New %s has been created. View this %s <a href="%s">here</a>.') % (_('people'), _('people'), '#')
        self.title = _('Create %s') % _('People')
        self.button = _('Save new')


class TestDeletePeople(TestDeleteDomain):

    inst_name = 'people'


class TestEditTopic(TestCase):

    def setUp(self):

        self.staff1 = factory.create_staff('staff', 'crosalot@kmail.com', 'password', ' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.topic2 = factory.create_topic(created_by=self.staff1)

        self.client.login(username=self.staff1.username, password='password')

        # Define for override
        self.check_initial = True
        self.topic1 = factory.create_topic(created_by=self.staff1)
        self.url1 = reverse('topic_edit', args=[self.topic1.id])
        self.url2 = reverse('topic_edit', args=[self.topic2.id])
        self.message_success = _('Your %s settings has been updated. View this %s <a href="%s">here</a>.') % (_('topic'), _('topic'), '#')
        self.title = _('Edit %s') % _('Topic')
        self.button = _('Save changes')



    def test_get_edit_page(self):

        self.client.logout()

        response = self.client.get(self.url1)
        self.assertRedirects(response, '%s?next=%s' % (reverse('account_login'), self.url1))

        self.client.login(username=self.staff1.username, password='password')
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'domain/topic_form.html')
        self.client.logout()

    def test_edit_context(self):
        response = self.client.get(self.url1)

        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'name="as_revision"')
        self.assertContains(response, self.title)
        self.assertContains(response, self.button)

        if not self.check_initial:
            return

        self.assertContains(response, self.topic1.title)
        self.assertContains(response, self.topic1.description)



        response = self.client.get(self.url2)
        self.assertContains(response, self.topic2.title)
        self.assertContains(response, self.topic2.description)

    def test_edit_post(self):

        params = {
            'title': self.topic1.title,
            'description': self.topic1.description,
        }

        response = self.client.post(self.url1, params, follow=True)


        if self.topic1.id:
            self.topic1 = Topic.objects.get(id=self.topic1.id)
        else:
            self.topic1 = Topic.objects.latest('id')

        self.assertContains(response, self.topic1.title)
        self.assertContains(response, self.topic1.description)
        self.assertContains(response, self.message_success)

        try:
            self.topic1 = Topic.objects.get(id=self.topic1.id)
        except: # For created
            self.topic1 = Topic.objects.latest('id')

        self.assertEqual(self.staff1, self.topic1.created_by)


    def test_has_new(self):
        before = Topic.objects.all().count()
        self.test_edit_post()
        after = Topic.objects.all().count()

        self.assertEqual(int(not self.check_initial), after-before)


    def test_post_edit_invalid(self):

        params = {
            'title': '',
            'description': '',
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'title', [_('This field is required.')])

        self.client.logout()

    def test_post_edit_not_update(self):

        params = {
            'title': self.topic1.title,

        }

        response = self.client.post(self.url1, params, follow=True)
        self.assertContains(response, self.message_success)

    def test_post_edit_without_revision(self):

        params = {
            'title': self.topic1.title,
            'description': self.topic1.description,
            'as_revision': False
        }

        before_count = self.topic1.topicrevision_set.count()

        response = self.client.post(self.url1, params, follow=True)


        self.assertContains(response, self.topic1.title)
        self.assertContains(response, self.topic1.description)
        self.assertContains(response, self.message_success)
        self.assertEqual(response.context['form'].initial['as_revision'], True)

        self.topic1 = Topic.objects.get(id=self.topic1.id)

        self.assertEqual(self.staff1, self.topic1.created_by)

        after_count = self.topic1.topicrevision_set.count()
        self.assertEqual(after_count, before_count)


class TestCreateTopic(TestEditTopic):

    def setUp(self):
        super(TestCreateTopic, self).setUp()

        self.check_initial = False

        self.topic1 = Topic(**{
            'title': 'New topic',
            'description': 'Work on opendream as topic',
        })
        self.url1 = reverse('topic_create')
        self.url2 = reverse('topic_create')
        self.message_success = _('New %s has been created. View this %s <a href="%s">here</a>.') % (_('topic'), _('topic'), '#')
        self.title = _('Create %s') % _('Topic')
        self.button = _('Save new')


    def test_edit_context(self):
        response = self.client.get(self.url1)

        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="description"')
        self.assertNotContains(response, 'name="as_revision"')
        self.assertContains(response, self.title)
        self.assertContains(response, self.button)

    def test_post_edit_without_revision(self):

        params = {
            'title': self.topic1.title,
            'description': self.topic1.description,
            'as_revision': False
        }

        response = self.client.post(self.url1, params, follow=True)


        self.assertContains(response, self.topic1.title)
        self.assertContains(response, self.topic1.description)
        self.assertContains(response, self.message_success)
        self.assertEqual(response.context['form'].initial['as_revision'], True)


        self.topic1 = Topic.objects.latest('id')

        self.assertEqual(self.staff1, self.topic1.created_by)

        after_count = self.topic1.topicrevision_set.count()
        self.assertEqual(1, after_count)


class TestDeleteTopic(TestDeleteDomain):

    inst_name = 'topic'


class TestEditStatement(TestCase):

    def setUp(self):

        self.people_category1 = factory.create_people_category('politician', 'Politician')
        self.people_category2 = factory.create_people_category('military', 'Military')

        self.staff1 = factory.create_staff(password='password')
        self.people1 = factory.create_people()
        self.topic1 = factory.create_topic()
        self.meter1 = factory.create_meter(permalink='unprovable')
        self.relate_statements1 = [factory.create_statement(tags=''), factory.create_statement(tags='')]
        self.relate_peoples1 = [factory.create_people(), factory.create_people()]


        self.statement2 = factory.create_statement()

        self.client.login(username=self.staff1.username, password='password')

        # Define for override
        self.check_initial = True
        self.statement1 = factory.create_statement(quoted_by=self.people1, created_by=self.staff1, topic=self.topic1, relate_statements=self.relate_statements1, relate_peoples=self.relate_peoples1)

        self.url1 = reverse('statement_edit', args=[self.statement1.id])
        self.url2 = reverse('statement_edit', args=[self.statement2.id])
        self.message_success = _('Your %s settings has been updated. View this %s <a href="%s">here</a>.') % (_('statement'), _('statement'), '#')
        self.title = _('Edit %s') % _('Statement')
        self.button = _('Save changes')

        # Add more

        self.references1 = {
            'references-TOTAL_FORMS': 4,
            'references-INITIAL_FORMS': len(self.statement1.references),
            'references-MAX_NUM_FORMS': 1000,
        }
        for i, reference in enumerate(self.statement1.references):
            self.references1['references-%d-title' % i] = reference['title']
            self.references1['references-%d-url' % i] = reference['url']

        self.references2 = {
            'references-TOTAL_FORMS': 4,
            'references-INITIAL_FORMS': len(self.statement2.references),
            'references-MAX_NUM_FORMS': 1000,
        }
        for i, reference in enumerate(self.statement2.references):
            self.references2['references-%d-title' % i] = reference['title']
            self.references2['references-%d-url' % i] = reference['url']


    def test_get_edit_page(self):

        self.client.logout()

        response = self.client.get(self.url1)
        self.assertRedirects(response, '%s?next=%s' % (reverse('account_login'), self.url1))

        self.client.login(username=self.staff1.username, password='password')
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'domain/statement_form.html')
        self.client.logout()

    def test_edit_context(self):
        response = self.client.get(self.url1)

        self.assertContains(response, 'name="permalink"')
        self.assertContains(response, 'name="quoted_by"')
        self.assertContains(response, 'name="quote"')
        self.assertContains(response, 'name="references-0-title"')
        self.assertContains(response, 'name="references-0-url"')
        self.assertContains(response, 'name="references-1-title"')
        self.assertContains(response, 'name="references-1-url"')
        self.assertContains(response, 'name="topic"')
        self.assertContains(response, 'name="tags"')
        self.assertContains(response, 'name="meter"')
        self.assertContains(response, 'name="relate_statements"')
        self.assertContains(response, 'name="relate_peoples"')
        self.assertContains(response, 'name="status"')
        self.assertContains(response, self.title)
        self.assertContains(response, self.button)

        if not self.check_initial:
            return

        self.assertContains(response, self.statement1.permalink)
        self.assertContains(response, self.statement1.quoted_by_id)
        self.assertContains(response, self.statement1.quote)
        self.assertEqual(int(response.context['form'].initial['meter']), self.statement1.meter_id)
        self.assertEqual(list(response.context['form'].initial['relate_statements']), self.relate_statements1)
        self.assertEqual(list(response.context['form'].initial['relate_peoples']), self.relate_peoples1)

        for reference in self.statement1.references:
            self.assertContains(response, reference['title'])
            self.assertContains(response, reference['url'])



        response = self.client.get(self.url2)
        self.assertContains(response, self.statement2.permalink)
        self.assertContains(response, self.statement2.quoted_by_id)
        self.assertContains(response, self.statement2.quote)
        self.assertEqual(int(response.context['form'].initial['meter']), self.statement2.meter_id)

        for reference in self.statement2.references:
            self.assertContains(response, reference['title'])
            self.assertContains(response, reference['url'])

    def test_edit_post(self):


        params = {
            'permalink': self.statement1.permalink,
            'quoted_by': self.statement1.quoted_by_id,
            'quote': self.statement1.quote,
            'topic': self.statement1.topic_id,
            'meter': self.statement1.meter_id,
            'relate_statements': [relate_statement.id for relate_statement in self.relate_statements1],
            'relate_peoples': [relate_people.id for relate_people in self.relate_peoples1],
            'status': self.statement1.status
        }
        params.update(self.references2)

        response = self.client.post(self.url1, params, follow=True)


        if self.statement1.id:
            self.statement1 = Statement.objects.get(id=self.statement1.id)
        else:
            self.statement1 = Statement.objects.latest('id')

        self.assertContains(response, self.statement1.permalink)
        self.assertContains(response, self.statement1.quote)

        # test reference

        self.assertEqual(int(response.context['form'].initial['quoted_by']), self.statement1.quoted_by_id)
        self.assertEqual(int(response.context['form'].initial['status']), self.statement1.status)
        self.assertEqual(int(response.context['form'].initial['topic']), self.statement1.topic_id)
        self.assertEqual(int(response.context['form'].initial['meter']), self.statement1.meter_id)
        self.assertEqual(list(response.context['form'].initial['relate_statements']), self.relate_statements1)
        self.assertEqual(list(response.context['form'].initial['relate_peoples']), self.relate_peoples1)

        self.assertEqual(response.context['reference_formset'].initial, self.statement1.references)
        self.assertEqual(2, len(self.statement1.references))

        #self.assertEqual(response.context['reference_formset'], 0)

    def test_edit_post_delete_reference(self):


        params = {
            'permalink': self.statement1.permalink,
            'quoted_by': self.statement1.quoted_by_id,
            'quote': self.statement1.quote,
            'topic': self.statement1.topic_id,
            'meter': self.statement1.meter_id,
            'relate_statements': [relate_statement.id for relate_statement in self.relate_statements1],
            'relate_peoples': [relate_statement.id for relate_statement in self.relate_peoples1],
            'status': self.statement1.status,
        }
        self.references2['references-0-DELETE'] = True
        params.update(self.references2)

        response = self.client.post(self.url1, params, follow=True)


        # test reference

        self.statement1 = Statement.objects.get(id=self.statement1.id)

        self.assertEqual(response.context['reference_formset'].initial, self.statement1.references)
        self.assertEqual(1, len(self.statement1.references))


    def test_has_new(self):
        before = Statement.objects.all().count()
        self.test_edit_post()
        after = Statement.objects.all().count()

        self.assertEqual(int(not self.check_initial), after-before)


    def test_post_edit_invalid(self):

        params = {
            'permalink': '',
            'quote': '',
            'status': 0,
        }



        params.update(self.references1)

        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink', [_('This field is required.')])
        self.assertFormError(response, 'form', 'quoted_by', [_('This field is required.')])
        self.assertFormError(response, 'form', 'quote', [_('This field is required.')])
        self.assertFormError(response, 'form', 'meter', [_('This field is required.')])


        params = {
            'permalink': self.statement2.permalink,
            'quoted_by': self.statement1.quoted_by_id,
            'quoted_by-autocomplete': self.statement1.quoted_by_id,
            'quote': self.statement1.quote,
            'meter': self.statement1.meter_id,
            'status': '',
        }
        params.update(self.references1)

        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink',  [_('This permalink is already in use.')])


        params = {
            'permalink': 'a tom in link?',
            'quoted_by': self.statement1.quoted_by_id,
            'quote': self.statement1.quote,
            'meter': self.statement1.meter_id,
            'status': '',
        }
        params.update(self.references1)

        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink',  [_('Enter a valid permalink.')])

        self.client.logout()

    def test_post_edit_not_update(self):

        params = {
            'permalink': self.statement1.permalink,
            'quoted_by': self.statement1.quoted_by_id,
            'quote': self.statement1.quote,
            'meter': self.statement1.meter_id,
            'status': self.statement1.status,
        }
        params.update(self.references1)

        response = self.client.post(self.url1, params, follow=True)

        self.assertContains(response, self.message_success)



class TestCreateStatement(TestEditStatement):

    def setUp(self):
        super(TestCreateStatement, self).setUp()


        self.check_initial = False
        self.statement1 = factory.create_statement(quoted_by=self.people1, created_by=self.staff1)
        self.statement1 = Statement(**{
            'permalink': 'new-statement',
            'quoted_by': self.people1,
            'created_by': self.staff1,
            'quote': 'New quote',
            'topic': self.topic1,
            'meter': self.meter1
        })

        self.url1 = reverse('statement_create')
        self.url2 = reverse('statement_create')
        self.message_success = _('New %s has been created. View this %s <a href="%s">here</a>.') % (_('statement'), _('statement'), '#')

        self.title = _('Create %s') % _('Statement')
        self.button = _('Save new')

    def test_edit_post_delete_reference(self):
        pass


class TestDeleteStatement(TestDeleteDomain):

    inst_name = 'statement'
