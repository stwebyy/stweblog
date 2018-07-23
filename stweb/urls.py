from django.urls import path

from . import views

app_name = 'stweb'
urlpatterns = [
    path('top/', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('category_detail/<int:pk>', views.category_detail, name='category_detail'),
]
