from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, FormView
from article.models import Category, Article, Tag
from user.models import User
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

from .forms import ContactForm


class IndexView(PaginationMixin, ListView):
    model = Article
    template_name = 'stweb/index.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_list = Article.objects.filter(publick=1).order_by('-created_at')
        paginator = Paginator(contact_list, 9)
        try:
            page = int(self.request.GET.get('page'))
        except:
            page = 1

        try:
            contact_list = paginator.page(page)
        except(EmptyPage, InvalidPage):
            contact_list = paginator.page(1)

        context['object_list'] = contact_list
        context['articles'] = Article.objects.filter(publick=1).order_by('-created_at')[:3]
        context['count'] = Article.objects.filter(publick=1).count()
        context['more_context'] = Category.objects.all()
        context['more_tags'] = Tag.objects.all()

        return context

index = IndexView.as_view()


class Detail(DetailView):
    model = Article
    template_name = 'stweb/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['more_context'] = Category.objects.all()
        context['more_tags'] = Tag.objects.all()
        return context

detail = Detail.as_view()

class CategoryDetail(DetailView):
    model = Category
    template_name = 'stweb/category_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = Article.objects.filter(category_id=self.object.id, publick=1).order_by('id')
        context['count'] = Article.objects.filter(category_id=self.object.id).filter(publick=1).count()
        context['more_context'] = Category.objects.all()
        context['more_tags'] = Tag.objects.all()
        return context

category_detail = CategoryDetail.as_view()


class TagDetail(DetailView):
    model = Tag
    template_name = 'stweb/tag_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = Tag.objects.get(id=self.object.id)
        context['more_context'] = Category.objects.all()
        context['more_tags'] = Tag.objects.all()
        return context

tag_detail = TagDetail.as_view()

class About(TemplateView):
    template_name = "stweb/about.html"

about = About.as_view()


class ContactView(FormView):
    template_name = 'stweb/contact.html'
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

contact = ContactView.as_view()
