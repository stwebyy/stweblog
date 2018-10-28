from django.db import models
from django.contrib import admin

from martor.widgets import AdminMartorWidget
from martor.models import MartorField

from .models import Tag, Category, Article


class ArticleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        MartorField: {'widget': AdminMartorWidget},
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(Article, ArticleModelAdmin)
admin.site.register(Category)
admin.site.register(Tag)
