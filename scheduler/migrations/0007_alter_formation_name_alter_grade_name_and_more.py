# Generated by Django 4.2.1 on 2023-05-28 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0006_remove_module_volume_enseignant_daily_load_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formation',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='grade',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='salle',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
