from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from .models import User
from .views import IndexView, LoginView, LogoutView, RegisterView, ProfileView
from .urls import *
from .forms import RegisterForm
from django.contrib.auth import login as auth_login, logout as auth_logout

import uuid


class Usermodel_assert(TestCase):
    def usermodel_assert(self, first_user, name, email, password):
        self.assertEqual(first_user.username, name)
        self.assertEqual(first_user.email, email)
        self.assertEqual(first_user.password, password)


class Usermodel_test(Usermodel_assert):
    def test_empty_usermodel(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 0)


    def test_notempty_usermodel(self, username=None, email=None, password=None):
        test_user = User()
        if username is not None:
            user.username = 'aaa'
        if email is not None:
            user.email = 'test'
        if password is not None:
            user.password = '1111'
        test_user.save()
        users = User.objects.all()
        self.assertEqual(users.count(), 1)


    def test_user_model(self):
        name = '20文字以内'
        email = 'a@gmail.com'
        password = '1111'
        user = User(
        username = name,
        email = email,
        password = password,
        )
        user.save()
        users = User.objects.all()
        first_user = users[0]
        self.assertEqual(users.count(), 1)


class Resolve_urls(TestCase):
    def test_url_index(self):
        found = resolve('/user/index/')
        self.assertEqual(found.func.view_class, IndexView)

    def test_url_login(self):
        found = resolve('/user/login/')
        self.assertEqual(found.func.view_class, LoginView)

    def test_url_register(self):
        found = resolve('/user/register/')
        self.assertEqual(found.func.view_class, RegisterView)

    def test_url_logout(self):
        found = resolve('/user/logout/')
        self.assertEqual(found.func.view_class, LogoutView)

    def test_url_profile(self):
        user = User()
        user.save()
        uuid = user.uuid
        url = '/user/profile/%s/' % uuid
        found = resolve(url)
        self.assertEqual(found.func.view_class, ProfileView)


class Views_tests(TestCase):
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


class Register_form_test(TestCase):
    def test_form_valid(self):
        params = dict(username='test', email="test@test.com", password="1111", password2="1111")
        form = RegisterForm(params)
        self.assertTrue(form.is_valid())

    def test_form_not_valid_username(self):
        params = dict(username='', email="test@test.com", password="1111", password2="1111")
        form = RegisterForm(params)
        self.assertFalse(form.is_valid())

    def test_form_not_valid_email(self):
        params = dict(username='test', email="", password="1111", password2="1111")
        form = RegisterForm(params)
        self.assertFalse(form.is_valid())

    def test_form_not_valid_password(self):
        params = dict(username='', email="test@test.com", password="1234", password2="1111")
        form = RegisterForm(params)
        self.assertFalse(form.is_valid())
