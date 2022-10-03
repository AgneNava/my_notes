from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('mynotes/', views.UserNotesListView.as_view(), name='mynotes'),
    path('mynotes/<int:pk>', views.UserNoteDetailView.as_view(), name='my-note'),
    path('search/', views.search, name='search'),
]