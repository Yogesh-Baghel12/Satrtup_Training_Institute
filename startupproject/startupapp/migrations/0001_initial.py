# Generated by Django 4.2.2 on 2023-09-04 13:25

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('courseName', models.CharField(max_length=150, primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='course')),
                ('courseFee', models.IntegerField()),
                ('courseDuration', models.IntegerField()),
                ('syllabus', ckeditor.fields.RichTextField(default='syllabus')),
                ('aboutCourse', ckeditor.fields.RichTextField(default='aboutCourse')),
                ('stars', models.IntegerField(default=3)),
            ],
        ),
    ]