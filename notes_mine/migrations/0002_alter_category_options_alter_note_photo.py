# Generated by Django 4.1.1 on 2022-10-02 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes_mine', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Kategorija', 'verbose_name_plural': 'Kategorijos'},
        ),
        migrations.AlterField(
            model_name='note',
            name='photo',
            field=models.ImageField(null=True, upload_to='images', verbose_name='Photo'),
        ),
    ]
