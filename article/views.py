import logging

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.db.models import F
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage, InvalidPage
from django.core.paginator import PageNotAnInteger
from pure_pagination.mixins import PaginationMixin

from .forms import PostForm, CategoryForm, EditForm, TagForm, TagSelectForm, TagInlineFormSet, ContactForm

from .models import Category, Article, Tag
from user.models import User



class IndexView(PaginationMixin, LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_list = Article.objects.filter(user_id=self.request.user.uuid).order_by('-created_at')
        paginator = Paginator(contact_list, 5)
        try:
            page = int(self.request.GET.get('page'))
        except:
            page = 1

        try:
            contact_list = paginator.page(page)
        except(EmptyPage, InvalidPage):
            contact_list = paginator.page(1)

        context['object_list'] = contact_list
        context['articles'] = Article.objects.filter(user_id=self.request.user.uuid).order_by('-created_at')[:5]
        context['count'] = Article.objects.filter(user_id=self.request.user.uuid).count()
        context['more_context'] = Category.objects.filter(user_id=self.request.user.uuid)
        context['more_tags'] = Tag.objects.all()
        return context

index = IndexView.as_view()


class Detail(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['more_context'] = Category.objects.all()
        context['more_tags'] = Tag.objects.all()
        return context

detail = Detail.as_view()


class PostView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = PostForm
    template_name = 'article/post.html'

    def post(self, request, *args, **kwargs):
        form_class = PostForm(request.POST)
        feed_cont = form_class.save(commit=False)
        formset = TagInlineFormSet(self.request.POST, instance=feed_cont)
        if not request.user.is_authenticated:
            messages.info(request, "ログインしてください。。。")
            return redirect('/user/login')
        feed_cont.user_id = request.user.uuid
        feed_cont.save()
        formset.save()
        return redirect('article:detail',pk=(feed_cont.id))

    success_url = "detail"

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = TagInlineFormSet(self.request.POST or None)
        return super().get_context_data(**kwargs)

post = PostView.as_view()


class EditView(UpdateView):
    model = Article
    form_class = EditForm
    template_name = "article/edit.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        formset = TagInlineFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            self.object.save()
            formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = TagInlineFormSet(self.request.POST or None, instance=self.object)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('article:detail',args=(self.object.id,))

edit = EditView.as_view()


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('article:index')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object.title))
        return result

article_delete = ArticleDeleteView.as_view()


class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'article/category_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = Article.objects.filter(category_id=self.object.id).order_by('id')
        context['more_context'] = Category.objects.filter(user_id=self.request.user.uuid)
        context['more_tags'] = Tag.objects.all()

        return context

category_detail = CategoryDetail.as_view()


class CategoryPostView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    categorys = Category.objects.all()
    template_name = 'article/category.post.html'
    success_url = "/article/index/"

    def post(self, request, *args, **kwargs):
        form_class = CategoryForm(request.POST)
        feed_cont = form_class.save(commit=False)
        if not request.user.is_authenticated:
            messages.info(request, "ログインしてください。。。")
            return redirect('/user/login')
        feed_cont.user_id = request.user.uuid
        feed_cont.save()
        return redirect('article:index')

    success_url = "index"


category_post = CategoryPostView.as_view()


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    form_class = CategoryForm

    success_url = reverse_lazy('article:index')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result

category_delete = CategoryDeleteView.as_view()



class TagDetail(LoginRequiredMixin, DetailView):
    model = Tag
    template_name = 'article/tag_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = Tag.objects.get(id=self.object.id)
        context['more_context'] = Category.objects.filter(user_id=self.request.user.uuid)
        context['more_tags'] = Tag.objects.all()
        return context

tag_detail = TagDetail.as_view()


class TagPostView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    tags = Tag.objects.all()
    template_name = 'article/tag.post.html'
    success_url = "/article/index/"

    def post(self, request, *args, **kwargs):
        form_class = TagForm(request.POST)
        feed_cont = form_class.save(commit=False)
        if not request.user.is_authenticated:
            messages.info(request, "ログインしてください。。。")
            return redirect('/user/login')
        feed_cont.user_id = request.user.uuid
        feed_cont.save()
        return redirect('article:index')

    success_url = "index"


tag_post = TagPostView.as_view()


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    form_class = TagForm

    success_url = reverse_lazy('article:index')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.success(
            self.request, '「{}」を削除しました'.format(self.object))
        return result

tag_delete = TagDeleteView.as_view()

class ContactView(FormView):
    template_name = 'article/contact.html'
    form_class = ContactForm
    success_url = "/stweb/top/"

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)

contact = ContactView.as_view()
