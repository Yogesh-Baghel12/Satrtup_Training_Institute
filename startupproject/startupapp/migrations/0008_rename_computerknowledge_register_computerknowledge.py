# Generated by Django 4.2.2 on 2023-09-07 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startupapp', '0007_rename_computerknowledge_register_computerknowledge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='computerknowledge',
            new_name='computerKnowledge',
        ),
    ]
