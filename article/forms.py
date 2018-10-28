from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import Article, Category, Tag


class PostForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'discript', 'thumnail', 'text', 'category', 'publick',)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control'}
        self.fields['discript'].widget.attrs = {'class': 'form-control'}
        self.fields['text'].widget.attrs = {'class': 'form-control'}
        self.fields['category'].widget.attrs = {'class': 'form-control'}
        self.fields['text'].widget.attrs = {'id': 'text-area'}


class TagSelectForm(forms.ModelForm):
    class Meta:
        model = Article.tag.through
        fields = ('tag',)
        widgets = {
            'tag': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

TagInlineFormSet = forms.inlineformset_factory(
    Article, Article.tag.through, form=TagSelectForm, can_delete=False
)


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class EditForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'discript', 'thumnail', 'text', 'category', 'publick',)

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control'}
        self.fields['discript'].widget.attrs = {'class': 'form-control'}
        self.fields['text'].widget.attrs = {'class': 'form-control'}
        self.fields['category'].widget.attrs = {'class': 'form-control'}
        self.fields['text'].widget.attrs = {'id': 'text-area'}
