# Generated by Django 3.2.8 on 2021-11-15 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20211114_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='current_city',
        ),
        migrations.RemoveField(
            model_name='user',
            name='hometown',
        ),
    ]
