from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36
from django.utils.translation import ugettext_lazy as _
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

    def test_post_login_with_email(self):
        params = {
            'email': self.staff.email,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params, follow=True)

        self.assertIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('domain_home'))
        self.client.logout()

    def test_post_login_with_username(self):
        params = {
            'email': self.staff.username,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params, follow=True)

        self.assertIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, reverse('domain_home'))
        self.client.logout()

    def test_post_login_invalid(self):
        # invalid username
        params = {
            'email': '%s.invalid' % self.staff.username,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params)

        self.assertContains(response, _('Please, enter correct email/username and password'))
        self.assertNotIn('_auth_user_id', self.client.session)

        # invalid password
        params = {
            'email': self.staff.username,
            'password': 'password.invalid',
        }
        response = self.client.post(reverse('account_login'), params)

        self.assertContains(response, _('Please, enter correct email/username and password'))
        self.assertNotIn('_auth_user_id', self.client.session)

        # invalid active
        self.staff.is_active = False
        self.staff.save()

        params = {
            'email': self.staff.username,
            'password': 'password',
        }
        response = self.client.post(reverse('account_login'), params)

        self.assertContains(response, _('This account not activated'))
        self.assertNotIn('_auth_user_id', self.client.session)



    def test_logout(self):
        self.client.login(email=self.staff.email, password='password')
        response = self.client.get(reverse('account_logout'))
        self.assertIsNone(self.client.session.get('_auth_user_id'))
        self.assertRedirects(response, reverse('account_login'))
        self.client.logout()


class TestResetPassword(TestCase):

    def setUp(self):
        self.staff = factory.create_staff('crosalot', 'crosalot@gmail.com', 'password')

    def test_anonymous_user_can_access_forget_password_page(self):
        response = self.client.get(reverse('account_reset_password'), follow=True)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'account/password_reset_form.html')

    def test_authenticated_user_cannot_access_forget_password_page(self):
        self.client.login(username=self.staff.username, password='password')
        response = self.client.get(reverse('account_reset_password'), follow=True)
        self.assertEqual(403, response.status_code)

    def test_forget_password_page_context(self):
        response = self.client.get(reverse('account_reset_password'), follow=True)
        self.assertContains(response, 'name="email"')

    def test_anonymous_user_can_request_password(self):
        params = {
            'email': self.staff.email,
        }
        response = self.client.post(reverse('account_reset_password'), params, follow=True)
        self.assertRedirects(response, reverse('account_reset_password_done'))

    def test_request_password_with_invalid_email(self):
        params = {
            'email': 'invalid',
        }
        response = self.client.post(reverse('account_reset_password'), params, follow=True)
        self.assertFormError(response, 'form', 'email', [_('Enter a valid email address.')])

    def test_request_password_with_email_that_not_in_system(self):
        params = {
            'email': 'invalid@gmail.com',
        }
        response = self.client.post(reverse('account_reset_password'), params, follow=True)
        self.assertFormError(response, 'form', 'email', [_('Your email address is not registered.')])

    def test_access_reset_password_confirm_form_link_in_email(self):
        uid = int_to_base36(self.staff.id)
        token = default_token_generator.make_token(self.staff)
        response = self.client.get(reverse('account_reset_password_confirm', args=[uid, token, ]), follow=True)
        self.assertRedirects(response, reverse('account_edit')+'?reset_password=True')
        self.assertContains(response, _('Please, change your password'))

    def test_invalid_uid_in_reset_password_confirm(self):
        uid = '42'
        token = '3ai-e84fa443f006ac46frvp'
        response = self.client.get(reverse('account_reset_password_confirm', args=[uid, token, ]))
        self.assertEqual(404, response.status_code)