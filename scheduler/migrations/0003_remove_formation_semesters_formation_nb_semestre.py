# Generated by Django 4.2.1 on 2023-05-22 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_rename_module_seance_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formation',
            name='semesters',
        ),
        migrations.AddField(
            model_name='formation',
            name='nb_semestre',
            field=models.IntegerField(default=2),
        ),
    ]
