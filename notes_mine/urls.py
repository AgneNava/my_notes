from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('mynotes/', views.UserNotesListView.as_view(), name='mynotes'),
    path('mynotes/<int:pk>', views.UserNoteDetailView.as_view(), name='my-note'),
    path('mynotes/new', views.UserNoteCreateView.as_view(), name='my-new-note'),
    path('mynotes/<int:pk>/update', views.NoteUpdateView.as_view(), name='my-note-update'),
    path('mynotes/<int:pk>/delete', views.NoteDeleteView.as_view(), name='my-note-delete'),
    path('search/', views.search, name='search'),
]