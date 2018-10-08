from django.test import TestCase, Client
from django.urls import reverse
from user.models import User
from user.views import IndexView, LoginView, LogoutView, RegisterView, ProfileView

import uuid


class Test_views(TestCase):
    @classmethod
    def setUpTestData(cls):
        s = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )

    def test_index_before_login(self):
        response = Client().get(reverse('user:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'not_login')

    def test_index_after_login(self):
        c = self.client
        c.login(username='test', password='1111')
        response = c.get(reverse('user:index'))
        self.assertQuerysetEqual(response.context['more_context'],[])
        self.assertEqual(response.context['count'], 0)

    def test_login(self):
        response = Client().get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        c = self.client
        miss_user = {
        'username' : 'uuuu',
        'password' : '0123456'
        }
        miss_response = c.post(reverse('user:login'), miss_user)
        self.assertEqual(miss_response.status_code, 200)
        self.assertContains(miss_response, 'alert-primary')
        login_user = {
        'username' : 'test',
        'password' : '1111'
        }
        response = c.post(reverse('user:login'), login_user)
        self.assertEqual(response.status_code, 302)

    def test_logout_before_login(self):
        response = Client().get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)

    def test_logout_after_login(self):
        c = self.client
        c.login(username='test', password='1111')
        uuid = User([0]).uuid
        url = '/user/profile/%s/' % uuid
        res = c.get(url)
        self.assertEqual(res.status_code, 200)
        logout = c.get(reverse('user:logout'))
        resp = c.get(url)
        self.assertEqual(resp.status_code, 302)

    def test_register(self):
        response = Client().get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        c = self.client
        miss_data = {
        'username' : 'testname',
        'email' : 'testname@test.com',
        'password' : '1234',
        'password2': '112345678',
        }
        response = c.post(reverse('user:register'), miss_data)
        self.assertEqual(response.status_code, 200)
        data = {
        'username' : 'testname',
        'email' : 'testname@test.com',
        'password' : '1234',
        'password2': '1234',
        }
        response = c.post(reverse('user:register'), data)
        self.assertEqual(response.status_code, 302)

    def test_profile_before_login(self):
        user = User()
        user.save()
        uuid = user.uuid
        url = '/user/profile/%s/' % uuid
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_after_login(self):
        c = self.client
        c.login(username='test', password='1111')
        uuid = User([0]).uuid
        url = '/user/profile/%s/' % uuid
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, User(username=('test')).username)
        data = {
        'username' : 'edit',
        'email' : 'edit@edit.com',
        'uuid' : uuid,
        }
        response2 = c.post(url, data=data)
        self.assertEqual(response2.status_code, 302)
