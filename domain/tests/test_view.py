from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.test import TestCase

from common import factory
from domain.models import People


class TestEditPeople(TestCase):

    def setUp(self):

        self.staff1 = factory.create_staff('staff', 'crosalot@kmail.com', 'password', ' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.people2 = factory.create_people('panudate',' Panudate', 'Vasinwattana', 'Tester', 'Unittest', 'http://opendream.in.th')

        self.client.login(username=self.staff1.username, password='password')

        # Define for override
        self.check_initial = True
        self.people1 = factory.create_people('crosalot',' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.url1 = reverse('people_edit', args=[self.people1.id])
        self.url2 = reverse('people_edit', args=[self.people2.id])
        self.message_success = _('Your settings has been updated.')



    def test_get_edit_people_page(self):

        self.client.logout()

        response = self.client.get(self.url1)
        self.assertRedirects(response, '%s?next=%s' % (reverse('account_login'), self.url1))

        self.client.login(username=self.staff1.username, password='password')
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'domain/people_form.html')
        self.client.logout()

    def test_edit_people_context(self):
        response = self.client.get(self.url1)

        self.assertContains(response, 'name="permalink"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="occupation"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'name="homepage_url"')

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

    def test_edit_people_post(self):

        params = {
            'permalink': self.people1.permalink,
            'first_name': self.people1.first_name,
            'last_name': self.people1.last_name,
            'occupation': self.people1.occupation,
            'description': self.people1.description,
            'homepage_url': self.people1.homepage_url,
        }

        response = self.client.post(self.url1, params, follow=True)


        self.assertContains(response, self.people1.permalink)
        self.assertContains(response, self.people1.first_name)
        self.assertContains(response, self.people1.last_name)
        self.assertContains(response, self.people1.occupation)
        self.assertContains(response, self.people1.description)
        self.assertContains(response, self.people1.homepage_url)
        self.assertContains(response, self.message_success)

    def test_has_new(self):
        before = People.objects.all().count()
        self.test_edit_people_post()
        after = People.objects.all().count()

        self.assertEqual(int(not self.check_initial), after-before)


    def test_post_edit_people_invalid(self):

        params = {
            'permalink': '',
            'first_name': '',
            'last_name': '',
            'occupation': '',
            'description': '',
            'homepage_url': '',
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink', [_('This field is required.')])
        self.assertFormError(response, 'form', 'first_name', [_('This field is required.')])
        self.assertFormError(response, 'form', 'last_name', [_('This field is required.')])


        params = {
            'permalink': self.people2.permalink,
            'first_name': self.people1.first_name,
            'last_name': self.people1.last_name,
            'occupation': '',
            'description': '',
            'homepage_url': '',
        }
        response = self.client.post(self.url1, params)
        self.assertFormError(response, 'form', 'permalink',  [_('This permalink is already in use.')])

        self.client.logout()

    def test_post_edit_profile_not_update(self):

        params = {
            'permalink': self.people1.permalink,
            'first_name': self.people1.first_name,
            'last_name': self.people1.last_name,
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
