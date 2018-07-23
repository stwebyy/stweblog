from django.shortcuts import render
from django.views.generic import ListView, DetailView
from article.models import Category, Article
from user.models import User
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class IndexView(ListView):
    model = Article
    template_name = 'stweb/index.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(publick=1).order_by('-created_at')[:3]
        context['count'] = Article.objects.filter(publick=1).count()
        context['more_context'] = Category.objects.all()
        # articles = Article.objects.filter(publick=1)
        # context['user_list'] = User.objects.filter(uuid=self.object.user_id)

        return context

index = IndexView.as_view()


class Detail(DetailView):
    model = Article
    template_name = 'stweb/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['more_context'] = Category.objects.all()
        return context


detail = Detail.as_view()


class List(ListView):
    model = Article
    template_name = 'stweb/list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = Article.objects.all().filter(publick=1).order_by('id')
        return context


list = List.as_view()


class CategoryDetail(DetailView):
    model = Category
    template_name = 'stweb/category_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = Article.objects.all().filter(category_id=self.object.id, publick=1).order_by('id')
        return context

category_detail = CategoryDetail.as_view()
