from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from PIL import Image

# Create your models here.

class Note(models.Model):
  title = models.CharField(_('Title'), max_length=200)
  photo = models.ImageField(_('Photo'), blank=True, null=True, upload_to="images",)
  text = models.TextField(_('Text'), max_length=2000)
  category = models.ManyToManyField('Category')
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.title

  class Meta:
    verbose_name = 'Zinute'
    verbose_name_plural = 'Zinutes'

  def display_category(self):
    return ', '.join(category.name for category in self.category.all()[:3])

  display_category.short_description = 'Kategorija'


class Category(models.Model):
  name = models.CharField(_('Name'), max_length=200)

  def __str__(self):
      return self.name

  class Meta:
    verbose_name = 'Kategorija'
    verbose_name_plural = 'Kategorijos'


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  photo = models.ImageField(default="default.png", upload_to="profile_pics",)

  def __str__(self):
    return f"{self.user.username} profile"

  class Meta:
      verbose_name = 'Profilis'
      verbose_name_plural = 'Profiliai'

  def save(self, *args, **kwargs):
      super().save(*args, **kwargs)
      img = Image.open(self.photo.path)
      if img.height > 300 or img.width > 300:
          output_size = (300, 300)
          img.thumbnail(output_size)
          img.save(self.photo.path)