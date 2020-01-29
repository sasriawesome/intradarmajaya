# Generated by Django 2.2.8 on 2020-01-27 06:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0006_auto_20200127_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lectureschedule',
            options={'verbose_name': 'Lecture Schedule', 'verbose_name_plural': 'Lecture Schedules'},
        ),
        migrations.AlterField(
            model_name='studentscore',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='Student'),
        ),
    ]
