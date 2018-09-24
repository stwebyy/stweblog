from django.test import TestCase, Client
from user.models import User
from article.models import Article, Category, Tag


class Test_models(TestCase):
    def test_empty_articlemodel(self):
        articles = Article.objects.all()
        self.assertEqual(articles.count(), 0)

    def test_notempty_articlemodel(self, title=None, discript=None, text=None):
        first_user = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        test_article = Article(user_id=first_user.uuid)
        if title is not None:
            test_article.title = 'aaa'
        if discript is not None:
            test_article.discript = 'テストのため'
        if text is not None:
            test_article.text = ' テスト用記事'
        test_article.save()
        articles = Article.objects.all()
        self.assertEqual(articles.count(), 1)

    def test_articlemodel_assert(self):
        first_user = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        title = 'aaa'
        discript = 'bbb'
        text = 'ccc'
        a = Article(
        title = title,
        discript = discript,
        text = text,
        user_id = first_user.uuid,
        )
        a.save()
        self.assertEqual(a.title, title)
        self.assertEqual(a.discript, discript)
        self.assertEqual(a.text, text)
        articles = Article.objects.all()
        self.assertEqual(articles.count(), 1)

    def test_empty_categorymodel(self):
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 0)

    def test_notempty_categorymodels(self, name=None):
        first_user = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        test_category = Category(user_id=first_user.uuid)
        if name is not None:
            test_category.name = 'aaa'
        test_category.save()
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 1)

    def test_categorymodel_assert(self):
        first_user = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        name = 'aaa'
        c = Category(
        name = name,
        user_id = first_user.uuid,
        )
        c.save()
        self.assertEqual(c.name, name)
        categories = Category.objects.all()
        self.assertEqual(categories.count(), 1)

    def test_empty_tagmodel(self):
        tags = Tag.objects.all()
        self.assertEqual(tags.count(), 0)

    def test_notempty_tagmodels(self, name=None):
        first_user = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        test_tag = Tag(user_id=first_user.uuid)
        if name is not None:
            test_tag.name = 'aaa'
        test_tag.save()
        tags = Tag.objects.all()
        self.assertEqual(tags.count(), 1)

    def test_categorymodel_assert(self):
        first_user = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        name = 'aaa'
        c = Tag(
        name = name,
        user_id = first_user.uuid,
        )
        c.save()
        self.assertEqual(c.name, name)
        tags = Tag.objects.all()
        self.assertEqual(tags.count(), 1)

    def test_categorymodels_relation(self):
        first_user = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        name = 'category'
        c = Category(
        name = name,
        user_id = first_user.uuid,
        )
        c.save()
        title = 'title'
        discript = 'discript'
        text = 'text'
        a = Article(
        title = 'title',
        discript = 'discript',
        text = 'text',
        user_id = first_user.uuid,
        category_id = c.id,
        )
        a.save()
        aa = Article(
        title = '2個目',
        discript = '説明',
        text = 'テキスト',
        user_id = first_user.uuid,
        category_id = c.id,
        )
        aa.save()
        tag = Tag(
        name='tag',
        user_id =first_user.uuid,
        )
        tag.save()
        a.tag.add(tag)
        aa.tag.add(tag)
        tags = a.tag.all()
        sv = tag.article_set.all()
        articles = Article.objects.all()
        self.assertEqual(a.title, title)
        self.assertEqual(a.discript, discript)
        self.assertEqual(a.text, text)
        self.assertEqual(a.category_id, 2)
        self.assertEqual(tags.count(), 1)
        self.assertEqual(sv.count(), 2)
        self.assertEqual(articles.count(), 2)
