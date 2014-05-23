from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.test import TestCase

from common import factory

class TestEditPeople(TestCase):

    def setUp(self):

        self.staff1 = factory.create_staff('staff', 'crosalot@kmail.com', 'password', ' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.people1 = factory.create_people('crosalot',' Crosalot', 'Opendream ', 'Developer', 'Opensource', 'http://opendream.co.th')
        self.people2 = factory.create_people('panudate',' Panudate', 'Vasinwattana', 'Tester', 'Unittest', 'http://opendream.in.th')

        self.client.login(username=self.staff1.username, password='password')


    def test_get_edit_people_page(self):

        self.client.logout()

        response = self.client.get(reverse('people_edit', args=[self.people1.id]))
        self.assertRedirects(response, '%s?next=%s' % (reverse('account_login'), reverse('people_edit', args=[self.people1.id])))

        self.client.login(username=self.staff1.username, password='password')
        response = self.client.get(reverse('people_edit', args=[self.people1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'domain/people_edit.html')
        self.client.logout()

    def test_edit_people_context(self):
        response = self.client.get(reverse('people_edit', args=[self.people1.id]))

        self.assertContains(response, 'name="permalink"')
        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="occupation"')
        self.assertContains(response, 'name="description"')
        self.assertContains(response, 'name="homepage_url"')

        self.assertContains(response, self.people1.permalink)
        self.assertContains(response, self.people1.first_name)
        self.assertContains(response, self.people1.last_name)
        self.assertContains(response, self.people1.occupation)
        self.assertContains(response, self.people1.description)
        self.assertContains(response, self.people1.homepage_url)


        response = self.client.get(reverse('people_edit', args=[self.people2.id]))
        self.assertContains(response, self.people2.permalink)
        self.assertContains(response, self.people2.first_name)
        self.assertContains(response, self.people2.last_name)
        self.assertContains(response, self.people2.occupation)
        self.assertContains(response, self.people2.description)
        self.assertContains(response, self.people2.homepage_url)

    def test_post_edit_people_invalid(self):
        self.client.login(username=self.staff1.email, password='password')

        params = {
            'permalink': '',
            'first_name': '',
            'last_name': '',
            'occupation': '',
            'description': '',
            'homepage_url': '',
        }
        response = self.client.post(reverse('people_edit', args=[self.people1.id]), params)
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
        response = self.client.post(reverse('people_edit', args=[self.people1.id]), params)
        self.assertFormError(response, 'form', 'permalink',  [_('This permalink is already in use.')])

        self.client.logout()

    def test_post_edit_profile_not_update(self):
        self.client.login(username=self.staff1.email, password='password')

        params = {
            'permalink': self.people1.permalink,
            'first_name': self.people1.first_name,
            'last_name': self.people1.last_name,
        }

        response = self.client.post(reverse('people_edit', args=[self.people1.id]), params, follow=True)
        self.assertContains(response, _('Your settings has been updated.'))