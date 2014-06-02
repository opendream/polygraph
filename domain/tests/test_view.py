from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.test import TestCase

from common import factory
from domain.models import People, Topic


class TestEditPeople(TestCase):

    def setUp(self):

        self.people_category1 = factory.create_people_category('politician', 'Politician')
        self.people_category2 = factory.create_people_category('military', 'Military')

        self.staff1 = factory.create_staff('staff', 'crosalot@kmail.com', 'password', ' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.people2 = factory.create_people('panudate',' Panudate', 'Vasinwattana', 'Tester', 'Unittest', 'http://opendream.in.th', category=self.people_category1)

        self.client.login(username=self.staff1.username, password='password')

        # Define for override
        self.check_initial = True
        self.people1 = factory.create_people('crosalot',' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th', category=self.people_category2)
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
        }

        response = self.client.post(self.url1, params, follow=True)


        self.assertContains(response, self.people1.permalink)
        self.assertContains(response, self.people1.first_name)
        self.assertContains(response, self.people1.last_name)
        self.assertContains(response, self.people1.occupation)
        self.assertContains(response, self.people1.description)
        self.assertContains(response, self.people1.homepage_url)
        self.assertContains(response, self.message_success)

        self.assertEqual(list(response.context['form'].initial['categories']), [self.people_category1])

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
        })
        self.url1 = reverse('people_create')
        self.url2 = reverse('people_create')
        self.message_success = _('New %s has been created. View this %s <a href="%s">here</a>.') % (_('people'), _('people'), '#')
        self.title = _('Create %s') % _('People')
        self.button = _('Save new')


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

        self.assertContains(response, 'name="permalink"')
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, self.title)
        self.assertContains(response, self.button)

        if not self.check_initial:
            return

        self.assertContains(response, self.topic1.permalink)
        self.assertContains(response, self.topic1.title)
        self.assertContains(response, self.topic1.description)



        response = self.client.get(self.url2)
        self.assertContains(response, self.topic2.permalink)
        self.assertContains(response, self.topic2.title)
        self.assertContains(response, self.topic2.description)

    def test_edit_post(self):

        params = {
            'permalink': self.topic1.permalink,
            'title': self.topic1.title,
            'description': self.topic1.description,
        }

        response = self.client.post(self.url1, params, follow=True)


        self.assertContains(response, self.topic1.permalink)
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
            'permalink': '',
            'title': '',
            'description': '',
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink', [_('This field is required.')])
        self.assertFormError(response, 'form', 'title', [_('This field is required.')])


        params = {
            'permalink': self.topic2.permalink,
            'title': self.topic1.title,
            'description': '',
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink',  [_('This permalink is already in use.')])


        params = {
            'permalink': 'a tom in link?',
            'title': self.topic1.title,
            'description': '',
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink',  [_('Enter a valid permalink.')])

        self.client.logout()

    def test_post_edit_not_update(self):

        params = {
            'permalink': self.topic1.permalink,
            'title': self.topic1.title,

        }

        response = self.client.post(self.url1, params, follow=True)
        self.assertContains(response, self.message_success)


class TestCreateTopic(TestEditTopic):

    def setUp(self):
        super(TestCreateTopic, self).setUp()

        self.check_initial = False

        self.topic1 = Topic(**{
            'permalink': 'new-topic',
            'title': 'New topic',
            'description': 'Work on opendream as topic',
        })
        self.url1 = reverse('topic_create')
        self.url2 = reverse('topic_create')
        self.message_success = _('New %s has been created. View this %s <a href="%s">here</a>.') % (_('topic'), _('topic'), '#')
        self.title = _('Create %s') % _('Topic')
        self.button = _('Save new')
