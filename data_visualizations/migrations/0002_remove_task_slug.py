# Generated by Django 4.2.11 on 2024-04-13 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_visualizations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='slug',
        ),
    ]
