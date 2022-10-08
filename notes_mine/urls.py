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
    path('mycategories/', views.UserCatListView.as_view(), name='mycategories'), 
    # path('mycategories/<int:category_id>', views.category_notes, name='my-category'),
    path('mycategories/<int:pk>', views.CatNotesListView.as_view(), name='my-category'),
    path('mycategories/new', views.UserCatCreateView.as_view(), name='my-new-category'),
    path('mycategories/<int:pk>/update', views.UserCatUpdateView.as_view(), name='my-category-update'),
    path('mynotes/<int:pk>/preview', views.UserCatDetailView.as_view(), name='my-category-preview'),
    path('mycategories/<int:pk>/delete', views.UserCatDeleteView.as_view(), name='my-category-delete'),
       
]