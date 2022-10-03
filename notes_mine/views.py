from multiprocessing import context
from django.urls import reverse, reverse_lazy
from turtle import title
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.views.generic.edit import FormMixin

from .models import Note, Profile, Category
# from .forms import RegistrationForm

# Create your views here.

def index(request):
    notes = Note.objects.all()
    return render(request, 'notes_mine/index.html', context={'notes': notes})



class UserNotesListView(LoginRequiredMixin,generic.ListView):
    model = Note
    context_object_name = 'notes'
    template_name ='notes_mine/user_notes.html'
   
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('title')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('notes_mine:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('notes_mine:register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, 'Registracija sekminga!')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('notes_mine:register')
    return redirect(request, 'notes_mine/register.html')

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             User.objects.create_user(username=form.cleaned_data['username'], 
#             email=form.cleaned_data['email'], 
#             password=form.cleaned_data['password'])   
#             messages.info(request, _('Registration successful!'))
#             return render(request, 'notes_mine/register.html')
#     else: 
#         form = RegistrationForm()

#     return render(request, 'notes_mine/register.html', {'form': form})


def search(request):
    query = request.GET.get('query')
    search_results = Note.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    return render(request, 'notes_mine/search.html', {'notes': search_results, 'query': query})