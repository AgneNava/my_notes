import django_filters

from .models import Note


class CatNotesFilter(django_filters.FilterSet):
    class Meta:
        model = Note
        fields = ['category']

    # Neveikia:
    # @property
    # def qs(self):
    #     parent = super().qs
    #     user = getattr(self.request, 'user', None)
    #     category = getattr(self.request, 'category', None)

    #     return parent.filter(category=category) \
    #         | parent.filter(user=user)