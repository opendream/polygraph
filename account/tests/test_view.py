# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse

from django.test import TestCase

from common import factory


class TestLogin(TestCase):
    def setUp(self):
        self.staff = factory.create_staff('crosalot', 'crosalot@gmail.com', 'password')

    def test_anonymous_get_login_page(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_authenticated_get_login_page_will_redirect_to_project_home(self):
        self.client.login(username=self.staff.username, password='password')

        response = self.client.get(reverse('account_login'), follow=True)
        self.assertRedirects(response, reverse('domain_home'))
        self.client.logout()

    def test_login_page_context(self):
        response = self.client.get(reverse('account_login'))
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')

    def test_post_login(self):
        params = {
            'email': self.staff.email,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params, follow=True)
        print self.client.session
        self.assertIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('domain_home'))
        self.client.logout()

    '''
    def test_logout(self):
        self.client.login(email=self.taeyeon.email, password='password')
        response = self.client.get(reverse('account_logout'))
        self.assertIsNone(self.client.session.get('_auth_user_id'))
        self.assertRedirects(response, reverse('account_login'))
        self.client.logout()
    '''