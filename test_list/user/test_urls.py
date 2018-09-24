from django.test import TestCase, Client
from django.urls import resolve
from user.models import User
from user.views import IndexView, LoginView, LogoutView, RegisterView, ProfileView


class Test_urls(TestCase):
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
