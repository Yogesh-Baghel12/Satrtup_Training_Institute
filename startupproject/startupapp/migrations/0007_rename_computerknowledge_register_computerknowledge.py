# Generated by Django 4.2.2 on 2023-09-07 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startupapp', '0006_payments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='computerKnowledge',
            new_name='computerknowledge',
        ),
    ]