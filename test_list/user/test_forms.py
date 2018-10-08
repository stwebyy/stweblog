from django.test import TestCase, Client
from user.models import User
from user.forms import RegisterForm, LoginForm, ProfileForm


class Test_forms(TestCase):
    @classmethod
    def setUpTestData(cls):
        s = User.objects.create_user(
        username = 'form',
        email = 'form@test.com',
        password = '1234',
        )

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

    def test_LoginForm(self):
        params = dict(username='form', password="1234")
        form = LoginForm(params)
        self.assertTrue(form.is_valid())

    def test_ProfileForm(self):
        params = dict(username='test', email="test@test.com")
        form = ProfileForm(params)
        self.assertTrue(form.is_valid())
        params2 = dict(username='form', email='form@test.com')
        form = ProfileForm(params2)
        self.assertFalse(form.is_valid())
