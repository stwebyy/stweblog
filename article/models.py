from django.db import models
from django.utils import timezone
from user.models import User


# TODO: class Tag(model.Models):
    # class Meta:
    #     db_table = tag
    # name = models.CharField('タグ名', max_length=50)
    # def __str__(self):
    #     return self.name


class Category(models.Model):
    class Meta:
        db_table = 'category'

    name = models.CharField('カテゴリ名', max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    class Meta:
        db_table = 'article'

    user = models.ForeignKey(User, verbose_name='ユーザーID', on_delete=models.CASCADE)
    title = models.CharField('タイトル', max_length=255)
    text = models.CharField('本文', max_length=10000)
    category = models.ForeignKey(Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
    thumnail = models.ImageField(
        'サムネイル', upload_to='post_thumbnail/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.name
