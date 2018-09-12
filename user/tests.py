from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.shortcuts import redirect
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import User
from .views import IndexView, LoginView, LogoutView, RegisterView, ProfileView
from .urls import *
import uuid


class Usermodel_assert(TestCase):
    def usermodel_assert(self, first_user, name, email, password):
        self.assertEqual(first_user.username, name)
        self.assertEqual(first_user.email, email)
        self.assertEqual(first_user.password, password)


class Users_test(Usermodel_assert):
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
        print(uuid)
        url = '/user/profile/%s/' % uuid
        print(url)
        found = resolve(url)
        self.assertEqual(found.func.view_class, ProfileView)


class Html_tests(TestCase):
    def test_index(self):
        response = Client().get(reverse('user:index'))
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = Client().get(reverse('user:login'))
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = Client().get(reverse('user:logout'))
        print(response)
        self.assertEqual(response.status_code, 302)

    def test_register(self):
        response = Client().get(reverse('user:register'))
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        user = User()
        user.save()
        uuid = user.uuid
        url = '/user/profile/%s/' % uuid
        print(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
