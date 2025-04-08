from django.contrib import admin
from django.urls import path, include
from . import views
# from .views import todo_list_create, todo_detail

urlpatterns = [
    path('', views.index, name='index'),
    path('todos/', views.todo_list_create, name='todo-list-create'),
    path('todos/<int:pk>/', views.todo_detail, name='todo-detail'),
    path('todo/<int:pk>/', views.todo_detail_view, name='todo_detail_view')
]
