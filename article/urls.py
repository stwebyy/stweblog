from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('post/', views.post, name='post'),
    path('list/', views.list, name='list'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('delete/<int:pk>', views.article_delete, name='article_delete'),
    path('category_detail/<int:pk>', views.category_detail, name='category_detail'),
    path('category/post', views.category_post, name='category_post'),
    path('category/delete/<int:pk>', views.category_delete, name='category_delete'),
    path('tag_detail/<int:pk>', views.tag_detail, name='tag_detail'),
    path('tag/post', views.tag_post, name='tag_post'),
    path('tag/delete/<int:pk>', views.tag_delete, name='tag_delete'),
]
