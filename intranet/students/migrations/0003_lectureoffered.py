# Generated by Django 2.2.10 on 2020-02-25 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0002_auto_20200226_0332'),
        ('intranet_students', '0002_studentenrollmentplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='LectureOffered',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('lectures.lecture',),
        ),
    ]
