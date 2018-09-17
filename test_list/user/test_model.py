from django.test import TestCase, Client
from user.models import User


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
