from multiprocessing import context
from django.urls import reverse, reverse_lazy
from turtle import title
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
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
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm, UserNoteCreateForm

# Create your views here.

def index(request):
    notes = Note.objects.all()
    return render(request, 'notes_mine/index.html', context={'notes': notes})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username=form.cleaned_data['username'], 
            email=form.cleaned_data['email'], 
            password=form.cleaned_data['password'])   
            messages.info(request, _('Registration successful!'))
            return render(request, 'notes_mine/register.html')
    else: 
        form = RegistrationForm()

    return render(request, 'notes_mine/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile renewed")
            return redirect('notes_mine:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)  
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'notes_mine/profile.html', context=context)

def search(request):
    query = request.GET.get('query')
    search_results = Note.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    return render(request, 'notes_mine/search.html', {'notes': search_results, 'query': query})


class UserNotesListView(LoginRequiredMixin,generic.ListView):
    model = Note
    context_object_name = 'note_list'
    template_name ='notes_mine/user_notes.html'
   
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class UserNoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Note
    template_name = 'notes_mine/user_note.html'


class UserNoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    form_class = UserNoteCreateForm
    template_name = 'notes_mine/user_note_form.html'

    # Vietoj success_url:
    def get_success_url(self):
        return reverse('notes_mine:mynotes')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Note
    fields = ['title', 'photo', 'category', 'text']
    template_name = 'notes_mine/user_note_form.html'

    def get_success_url(self):
        return reverse('notes_mine:mynotes')

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Note
    success_url = reverse_lazy('notes_mine:mynotes')
    template_name = 'notes_mine/user_note_delete.html'

    # Testas tas pats
    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user


class UserCatListView(LoginRequiredMixin,generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name ='notes_mine/user_categories.html'
   
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class UserCatDetailView(LoginRequiredMixin, generic.DetailView):
    model = Category
    template_name = 'notes_mine/user_categories.html'