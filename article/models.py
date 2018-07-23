from django.db import models
from django.utils import timezone
from user.models import User
from django.utils.html import mark_safe
from markdown import markdown



class Tag(models.Model):
    class Meta:
        db_table = 'tag'
    name = models.CharField('タグ名', max_length=50)
    user = models.ForeignKey(User, verbose_name='ユーザーID', on_delete=models.CASCADE)


    def article_find(self):
        article = Article.objects.filter(tag=self)
        return article

    def tag_count(self):
        count = Article.objects.filter(tag=self).count()
        return count

    def tag_count_publick(self):
        count = Article.objects.filter(tag=self).count()
        return count

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        db_table = 'category'

    name = models.CharField('カテゴリ名', max_length=50)
    user = models.ForeignKey(User, verbose_name='ユーザーID', on_delete=models.CASCADE)

    def article_count(self):
        count = Article.objects.filter(category_id=self.id).count()
        return count

    def article_count_publick(self):
        count = Article.objects.filter(category_id=self.id, publick=1).count()
        return count

    def __str__(self):
        return self.name

class Article(models.Model):
    class Meta:
        db_table = 'article'

    user = models.ForeignKey(User, verbose_name='ユーザーID', on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=255)
    discript = models.TextField('概要', max_length=10000)
    text = models.TextField('本文', max_length=10000)
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='タグ')
    thumnail = models.ImageField(
        'サムネイル', upload_to='post_thumbnail/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateField('作成日', default=timezone.now)
    updated_at = models.DateField(auto_now=True)
    publick = models.BooleanField('公開・非公開（チェックすると公開します）', default=True)

    def get_text_as_markdown(self):
        return mark_safe(markdown(self.text, safe_mode='escape'))

    def user_find(self):
        find = User.objects.filter(uuid=self.user_id).values('username')
        return find

    def category_find(self):
        s = Category.objects.filter(id=self.category_id).get()
        return s

    def tag_find(self):
        s = Tag.objects.filter(article=self)
        return s


    def __str__(self):
        return self.title
