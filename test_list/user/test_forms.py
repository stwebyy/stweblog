from django.test import TestCase, Client
from user.models import User
from user.forms import RegisterForm


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
