from django.contrib import admin
from .models import Note, Category, Profile

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
  list_display = ('title', 'text', 'display_category', 'user',)
  list_filter = ('category__name',)


admin.site.register(Note, NoteAdmin)
admin.site.register(Category)
admin.site.register(Profile)
