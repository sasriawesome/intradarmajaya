# Generated by Django 2.2.8 on 2020-01-27 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0008_auto_20200127_1407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentattendance',
            options={'verbose_name': 'Student Attendance', 'verbose_name_plural': 'Student Attendances'},
        ),
        migrations.AlterModelOptions(
            name='teacherattendance',
            options={'verbose_name': 'Teacher Attendance', 'verbose_name_plural': 'Teacher Attendances'},
        ),
    ]
