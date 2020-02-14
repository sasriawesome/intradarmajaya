# Generated by Django 2.2.8 on 2020-02-07 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0005_auto_20200207_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_teacher_applicant',
        ),
        migrations.AlterField(
            model_name='person',
            name='is_employee_applicant',
            field=models.BooleanField(default=False, verbose_name='Employee applicant'),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_matriculant',
            field=models.BooleanField(default=False, verbose_name='Matriculant'),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_partner_applicant',
            field=models.BooleanField(default=False, verbose_name='Partner applicant'),
        ),
    ]