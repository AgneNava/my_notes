# from multiprocessing import context
# from unicodedata import category
from unicodedata import category
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
from .forms import RegistrationForm, UserCatCreateForm, UserUpdateForm, ProfileUpdateForm, UserNoteCreateForm
from .filters import CatNotesFilter

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
            messages.info(request, _('Wrong data entered. Please try again'))
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

    
    def get_success_url(self):
        return reverse('notes_mine:mynotes')

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UserNoteCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



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
    template_name = 'notes_mine/user_category_preview.html'

class UserCatCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    form_class = UserCatCreateForm
    template_name = 'notes_mine/user_category_form.html'

    def get_success_url(self):
        return reverse('notes_mine:mycategories-edit')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UserCatUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Category
    fields = ['name']
    template_name = 'notes_mine/user_category_form.html'

    def get_success_url(self):
        return reverse('notes_mine:mycategories-edit')

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user

class UserCatDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Category
    
    template_name = 'notes_mine/user_category_delete.html'
  
    def get_success_url(self):
        return reverse('notes_mine:mycategories-edit')

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user



class CatNotesListView(LoginRequiredMixin,generic.ListView):
    model = Note
    template_name = "notes_mine/category_notes.html"
    context_object_name = 'cat_notes'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('category__name')


@login_required
def notes_list(request):
    filter = CatNotesFilter(request.GET, queryset=Note.objects.all())
    return render(request, 'notes_mine/cat-notes-filtered.html', {'filter': filter})

    
   

