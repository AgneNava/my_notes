import django_filters

from .models import Note


class CatNotesFilter(django_filters.FilterSet):
    class Meta:
        model = Note
        fields = ['category']