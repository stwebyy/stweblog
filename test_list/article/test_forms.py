from django.test import TestCase, Client
from user.models import User
from article.models import Article, Category, Tag
from article.forms import PostForm, TagSelectForm, CategoryForm, TagForm, EditForm, ContactForm
from django.utils import timezone


class Test_PostForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(
        username = 'test',
        email = 'test@test.com',
        password = '1111',
        )
        u.save()
        a =Article.objects.create(
        title = 'aaa',
        discript = 'testdiscript',
        text = 'testtext',
        user_id = u.uuid,
        )
        a.save()
        c =  Category.objects.create(
        name = 'cate1',
        user_id = u.uuid,
        )
        c.save()
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

    def test_postform_valid(self):
        uuu = User(username="test")
        params = dict(title='タイトル欄', discript='説明文', thumnail=None, text='テキスト本文', category=1, publick='')
        form = PostForm(params)
        self.assertTrue(form.is_valid())

    def test_postform_not_valid_title(self):
        params = dict(title='', discript='説明文', thumnail=None, text='テキスト本文', category=1, publick=1)
        form = PostForm(params)
        self.assertFalse(form.is_valid())

    def test_postform_not_valid_discript(self):
        params = dict(title='タイトル欄', discript='', thumnail=None, text='テキスト本文', category=1, publick=1)
        form = PostForm(params)
        self.assertFalse(form.is_valid())

    def test_postform_not_valid_text(self):
        params = dict(title='タイトル欄', discript='説明文', thumnail=None, text='', category=1, publick=1)
        form = PostForm(params)
        self.assertFalse(form.is_valid())

    def test_postform_not_valid_category(self):
        params = dict(title='タイトル欄', discript='説明文', thumnail=None, text='テキスト本文', category='', publick=1)
        form = PostForm(params)
        self.assertFalse(form.is_valid())

    def test_categoryform_valid(self):
        params = dict(name='testname')
        form = CategoryForm(params)
        self.assertTrue(form.is_valid())

    def test_categoryform_not_valid(self):
        params = dict(name='')
        form = CategoryForm(params)
        self.assertFalse(form.is_valid())

    def test_tagyform_valid(self):
        params = dict(name='testname')
        form = TagForm(params)
        self.assertTrue(form.is_valid())

    def test_tagorm_not_valid(self):
        params = dict(name='')
        form = TagForm(params)
        self.assertFalse(form.is_valid())

    def test_editform_valid(self):
        params = dict(title='aaa', discript="testdiscript", text='testtext', category=1 ,thumnail='None', publick=1)
        form = EditForm(params)
        self.assertTrue(form.is_valid())

    def test_editform_not_valid_title(self):
        params = dict(title='', discript='説明文', thumnail=None, text='テキスト本文', category=1, publick=1)
        form = EditForm(params)
        self.assertFalse(form.is_valid())

    def test_editform_not_valid_discript(self):
        params = dict(title='タイトル欄', discript='', thumnail=None, text='テキスト本文', category=1, publick=1)
        form = EditForm(params)
        self.assertFalse(form.is_valid())

    def test_editform_not_valid_text(self):
        params = dict(title='タイトル欄', discript='説明文', thumnail=None, text='', category=1, publick=1)
        form = EditForm(params)
        self.assertFalse(form.is_valid())

    def test_editform_not_valid_category(self):
        params = dict(title='タイトル欄', discript='説明文', thumnail=None, text='テキスト本文', category='', publick=1)
        form = EditForm(params)
        self.assertFalse(form.is_valid())

    def test_contactform_valid(self):
        params = dict(name='test', message="メッセージ")
        form = ContactForm(params)
        self.assertTrue(form.is_valid())

    def test_contactform_notvalid(self):
        params = dict(name='', message="メッセージ")
        form = ContactForm(params)
        self.assertFalse(form.is_valid())

    def test_contactform_valid(self):
        params = dict(name='test', message="")
        form = ContactForm(params)
        self.assertFalse(form.is_valid())

    def test_tagselectform_valid(self):
        params = dict(tag=1)
        form = TagSelectForm(params)
        self.assertTrue(form.is_valid())

    def test_tagselectform_notvalid(self):
        params = dict(tag=3)
        form = TagSelectForm(params)
        self.assertFalse(form.is_valid())
