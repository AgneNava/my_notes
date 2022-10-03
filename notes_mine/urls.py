from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('my_notes/', views.UserNotesListView.as_view(), name='my_notes'),
    path('search/', views.search, name='search'),
]