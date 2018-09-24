from django.test import TestCase, Client
from django.urls import resolve
from article.models import Article, Category, Tag
from user.models import User
from article.views import IndexView, Detail, PostView, EditView, ArticleDeleteView, CategoryDetail, CategoryPostView, CategoryDeleteView, TagDetail, TagPostView, TagDeleteView, ContactView

import uuid


class Test_urls(TestCase):
    @classmethod
    def setUpTestData(cls):
        s = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        a =Article.objects.create(
        title = 'aaa',
        user_id = s.uuid,
        )
        c =  Category.objects.create(
        name = 'cate1',
        user_id = s.uuid,
        )
        t = Tag.objects.create(
        name = 'tag1',
        user_id = s.uuid,
        )
    def test_url_index(self):
        found = resolve('/article/index/')
        self.assertEqual(found.func.view_class, IndexView)

    def test_Detail(self):
        pk = 1
        url = '/article/detail/%s' % pk
        found = resolve(url)
        self.assertEqual(found.func.view_class, Detail)

    def test_Postview(self):
        found = resolve('/article/post/')
        self.assertEqual(found.func.view_class, PostView)

    def test_Editview(self):
        pk = 1
        url = '/article/edit/%s' % pk
        found = resolve(url)
        self.assertEqual(found.func.view_class, EditView)

    def test_ArticleDeleteView(self):
        pk = 1
        url = '/article/delete/%s' % pk
        found = resolve(url)
        self.assertEqual(found.func.view_class, ArticleDeleteView)

    def test_CategoryDetail(self):
        pk = 1
        url = '/article/category_detail/%s' % pk
        found = resolve(url)
        self.assertEqual(found.func.view_class, CategoryDetail)

    def test_CategoryPostView(self):
        found = resolve('/article/category/post')
        self.assertEqual(found.func.view_class, CategoryPostView)

    def test_CategoryDeleteView(self):
        pk = 1
        url = '/article/category/delete/%s' % pk
        found = resolve(url)
        self.assertEqual(found.func.view_class, CategoryDeleteView)

    def test_TagDetail(self):
        pk = 1
        url = '/article/tag_detail/%s' % pk
        found = resolve(url)
        self.assertEqual(found.func.view_class, TagDetail)

    def test_TagPostView(self):
        found = resolve('/article/tag/post')
        self.assertEqual(found.func.view_class, TagPostView)

    def test_TagDeleteView(self):
        pk = 1
        url = '/article/tag/delete/%s' % pk
        found = resolve(url)
        self.assertEqual(found.func.view_class, TagDeleteView)

    def test_ContactView(self):
        found = resolve('/article/contact/')
        self.assertEqual(found.func.view_class, ContactView)
