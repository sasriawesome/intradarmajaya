# Generated by Django 2.2.10 on 2020-02-25 03:52

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lectures', '0001_initial'),
        ('students', '0004_student_coach'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureForStudent',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('lectures.lecture',),
        ),
        migrations.CreateModel(
            name='ScheduleForStudent',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('lectures.lectureschedule',),
        ),
        migrations.CreateModel(
            name='ScoreForStudent',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('students.studentscore',),
            managers=[
                ('alt_manager', django.db.models.manager.Manager()),
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
