# Generated by Django 4.2.11 on 2024-04-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_visualizations', '0004_rename_datetime_task_uploaded_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='label',
            field=models.CharField(max_length=50, null=True),
        ),
    ]