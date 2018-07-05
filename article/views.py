import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

# from .models import Article

logger = logging.getLogger(__name__)


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.select_related('publisher').prefetch_related('authors').order_by('publish_date')
        keyword = request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )
        context = {
            'keyword': keyword,
            'book_list': queryset,
        }
        return render(request, 'shop/book_list.html', context)


index = IndexView.as_view()
