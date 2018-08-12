from django.urls import path

from . import views

app_name = 'stweb'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('category_detail/<int:pk>', views.category_detail, name='category_detail'),
    path('tag_detail/<int:pk>', views.tag_detail, name='tag_detail'),
]
