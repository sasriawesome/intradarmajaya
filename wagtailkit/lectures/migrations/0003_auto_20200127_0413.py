# Generated by Django 2.2.8 on 2020-01-26 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0002_lectureschedule_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lectureschedule',
            name='type',
            field=models.CharField(choices=[('MEETING', 'Meeting'), ('ELEARNING', 'E-Learning'), ('SUBTITUTE', 'Subtitution'), ('MID_EXAM', 'Mid Exam'), ('FINAL_EXAM', 'Final Exam')], default='MEETING', max_length=3, verbose_name='Type'),
        ),
    ]
