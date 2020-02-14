# Generated by Django 2.2.8 on 2020-01-29 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0001_initial'),
        ('attendances', '0002_auto_20200130_0421'),
        ('students', '0001_initial'),
        ('lectures', '0002_auto_20200130_0421'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherattendance',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers.Teacher', verbose_name='Teacher'),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lectures.LectureSchedule', verbose_name='Schedule'),
        ),
        migrations.AddField(
            model_name='studentattendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='Student'),
        ),
        migrations.AlterUniqueTogether(
            name='teacherattendance',
            unique_together={('schedule', 'teacher')},
        ),
        migrations.AlterUniqueTogether(
            name='studentattendance',
            unique_together={('schedule', 'student')},
        ),
    ]