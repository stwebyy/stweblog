from django.test import TestCase, Client
from django.urls import reverse
from user.models import User
from article.models import Article, Category, Tag
from article.views import IndexView, Detail, PostView, EditView, ArticleDeleteView, CategoryDetail, CategoryPostView, CategoryDeleteView, TagDetail, TagPostView, TagDeleteView, ContactView
from article.forms import PostForm, TagSelectForm, CategoryForm, TagForm, EditForm, ContactForm


class MyException(Exception):
  pass

class Target:
  def something(self):
    raise MyException


class Test_views(TestCase):
    def setUp(self):
        self.target = Target()

    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        u.save()
        c =  Category.objects.create(
        name = 'cate1',
        user_id = u.uuid,
        )
        c.save()
        print(c.id)
        a =Article.objects.create(
        title = 'aaa',
        discript = 'testdiscript',
        text = 'testtext',
        user_id = u.uuid,
        category = c,
        )
        a.save()
        print(a.id)
        aa =Article.objects.create(
        title = 'bbbb',
        discript = 'tesbbtdiscript',
        text = 'tbbbesttext',
        user_id = u.uuid,
        category = c,
        )
        aa.save()
        t = Tag.objects.create(
        name = 'tag1',
        user_id = u.uuid,
        )
        t.save()
        t2 = Tag.objects.create(
        name = 'tag2',
        user_id = u.uuid,
        )
        t2.save()
        print(t2.id)
        a.tag.add(t2)
        print(a.tag.all())

    def test_Indexview(self):
        response = Client().get(reverse('article:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/index/')
        c = self.client
        c.login(username='test', password='1111')
        response2 = c.get(reverse('article:index'))
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'category-link')

    def test_Detail(self):
        response = Client().get(reverse('article:detail', kwargs={'pk': 7}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/detail/7')
        c = self.client
        c.login(username='test', password='1111')
        response2 = c.get(reverse('article:detail', kwargs={'pk': 7}))
        self.assertEqual(response2.status_code, 200)
        response2 = c.get(reverse('article:detail', kwargs={'pk': 0}))
        self.assertEqual(response2.status_code, 404)

    def test_Postview(self):
        response = Client().get(reverse('article:post'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/post/')
        c = self.client
        c.login(username='test', password='1111')
        response2 = c.get(reverse('article:post'))
        self.assertEqual(response2.status_code, 200)
        print(Article.objects.all())
        uuid = User.objects.get(username='test').uuid
        data = {
        'title' : 'タイトル',
        'discript' : '説明文',
        'text' : '本文',
        'category' : 5,
        'user_id' : uuid,
        'Article_tag-TOTAL_FORMS' : 3,
        'Article_tag-INITIAL_FORMS' : 0,
        'Article_tag-MIN_NUM_FORMS': 0,
        'Article_tag-MAX_NUM_FORMS' : 0,
        }
        post = c.post(reverse('article:post'), data=data)
        all = Article.objects.all().count()
        self.assertEqual(post.status_code, 302)
        self.assertRedirects(post, '/article/detail/10')
        self.assertEqual(all, 3)

    def test_EditView(self):
        response = Client().get(reverse('article:edit', kwargs={'pk': 7}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/edit/7')
        c = self.client
        c.login(username='test', password='1111')
        response2 = c.get(reverse('article:edit', kwargs={'pk': 7}))
        self.assertEqual(response2.status_code, 200)
        data = {
        'title' : '変更後タイトル',
        'discript' : '変更後説明文',
        'text' : '変更後本文',
        'category' : 5,
        'Article_tag-TOTAL_FORMS' : 3,
        'Article_tag-INITIAL_FORMS' : 0,
        'Article_tag-MIN_NUM_FORMS': 0,
        'Article_tag-MAX_NUM_FORMS' : 0,
        }
        post_test = c.post(reverse('article:edit', kwargs={'pk': 7}), data)
        self.assertEqual(post_test.status_code, 302)
        self.assertRedirects(post_test, '/article/detail/7')
        data2 = {
        'title' : '',
        'discript' : '変更後説明文',
        'text' : '変更後本文',
        'category' : 5,
        'Article_tag-TOTAL_FORMS' : 3,
        'Article_tag-INITIAL_FORMS' : 0,
        'Article_tag-MIN_NUM_FORMS': 0,
        'Article_tag-MAX_NUM_FORMS' : 0,
        }
        post_test_nottitle = c.post(reverse('article:edit', kwargs={'pk': 7}), data2)
        self.assertEqual(post_test_nottitle.status_code, 200)
        self.assertContains(post_test_nottitle, '記事編集')

    def test_ArticleDeleteView(self):
        response = Client().get('/article/delete/9')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/delete/9')
        c = self.client
        c.login(username='test', password='1111')
        u = User.objects.get(username='test')
        create = Article.objects.create(
        title = 'delete_only',
        discript = 'testonly',
        text = 'only',
        user_id = u.uuid,
        category = Category(id=5),
        )
        response = c.delete('/article/delete/9')
        all = Article.objects.all().count()
        self.assertEqual(all, 2)

    def test_ArticleDeleteView_notdata(self):
        c = self.client
        c.login(username='test', password='1111')
        response = c.delete('/article/delete/1')
        self.assertEqual(response.status_code, 404)

    def test_CategoryDetail_notdata(self):
        response = Client().get(reverse('article:category_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/category_detail/1')
        c = self.client
        c.login(username='test', password='1111')
        response = c.get(reverse('article:category_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_CategoryDetail(self):
        response = Client().get(reverse('article:category_detail', kwargs={'pk': 5}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/category_detail/5')
        c = self.client
        c.login(username='test', password='1111')
        response = c.get(reverse('article:category_detail', kwargs={'pk': 5}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Category(id=5).name)
        self.assertContains(response, Article(id=7).title)

    def test_CategoryPostView(self):
        response = Client().get(reverse('article:category_post'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/category/post')
        c = self.client
        c.login(username='test', password='1111')
        response2 = c.get(reverse('article:category_post'))
        self.assertEqual(response2.status_code, 200)
        uuid = User.objects.get(username='test').uuid
        data = {
        'name' : 'cate2',
        'uuid' : uuid,
        }
        post_test = c.post(reverse('article:category_post'), data)
        self.assertEqual(post_test.status_code, 302)
        self.assertRedirects(post_test, '/article/index/')

    def test_CategoryDeleteView(self):
        c = self.client
        c.login(username='test', password='1111')
        u = User.objects.get(username='test')
        create = Category.objects.create(
        name = 'cccc',
        user_id = u.uuid
        )
        all = Category.objects.all().count()
        response = c.delete('/article/category/delete/6')
        all = Category.objects.all().count()
        self.assertEqual(all, 1)

    def test_Tagdetail_notdata(self):
        response = Client().get(reverse('article:tag_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/tag_detail/1')
        c = self.client
        c.login(username='test', password='1111')
        response = c.get(reverse('article:tag_detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_Tagdetail(self):
        response = Client().get(reverse('article:tag_detail', kwargs={'pk': 8}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/tag_detail/8')
        c = self.client
        c.login(username='test', password='1111')
        response = c.get(reverse('article:tag_detail', kwargs={'pk': 8}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Category(id=8).name)
        self.assertContains(response, Article(id=7).title)

    def test_TagPostView(self):
        response = Client().get(reverse('article:tag_post'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/user/login/?next=/article/tag/post')
        c = self.client
        c.login(username='test', password='1111')
        response2 = c.get(reverse('article:tag_post'))
        self.assertEqual(response2.status_code, 200)
        uuid = User.objects.get(username='test').uuid
        data = {
        'name' : 'taag2',
        'uuid' : uuid,
        }
        post_test = c.post(reverse('article:tag_post'), data)
        self.assertEqual(post_test.status_code, 302)
        self.assertRedirects(post_test, '/article/index/')

    def test_TagDeleteView(self):
        c = self.client
        c.login(username='test', password='1111')
        u = User.objects.get(username='test')
        create = Tag.objects.create(
        name = 'tttt',
        user_id = u.uuid
        )
        all1 = Tag.objects.all().count()
        self.assertEqual(all1, 3)
        response = c.delete('/article/tag/delete/9')
        all2 = Tag.objects.all().count()
        self.assertEqual(all2, 2)

    def test_ContactView(self):
        c = self.client
        response = c.get(reverse('article:contact'))
        self.assertEqual(response.status_code, 200)
        data = {
        'name' : 'test',
        'message' : 'test contact',
        }
        post_test = c.post(reverse('article:contact'), data)
        self.assertEqual(post_test.status_code, 302)
        self.assertRedirects(post_test, '/')
