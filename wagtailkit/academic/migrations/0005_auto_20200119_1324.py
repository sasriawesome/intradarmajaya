# Generated by Django 2.2.8 on 2020-01-19 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0004_auto_20200119_1317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curriculumcourse',
            name='rmu',
        ),
        migrations.AlterField(
            model_name='curriculum',
            name='prodi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.ProgramStudy', verbose_name='Program Study'),
        ),
        migrations.AlterField(
            model_name='schoolyear',
            name='semester',
            field=models.CharField(choices=[('1', 'Odd'), ('2', 'Even'), ('3', 'Short')], default='1', max_length=2, verbose_name='Semester'),
        ),
    ]
