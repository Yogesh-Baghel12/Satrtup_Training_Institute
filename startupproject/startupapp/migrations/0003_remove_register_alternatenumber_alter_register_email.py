# Generated by Django 4.2.2 on 2023-09-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startupapp', '0002_trainer_register'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='alternateNumber',
        ),
        migrations.AlterField(
            model_name='register',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
