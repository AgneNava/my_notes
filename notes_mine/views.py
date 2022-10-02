from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Note, Profile, Category

# Create your views here.

def index(request):
  return render(request, 'notes_mine/index.html')


class UserNotesListView(LoginRequiredMixin,generic.ListView):
    model = Note
    context_object_name = 'notes'
    template_name ='notes_mine/user_notes.html'
   
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('title')