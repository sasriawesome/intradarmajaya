# Generated by Django 2.2.8 on 2020-01-27 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0009_auto_20200127_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherattendance',
            name='status',
            field=models.CharField(choices=[('PR', 'Present'), ('SC', 'Sict'), ('AB', 'Absent'), ('PR', 'Permit')], default='PR', max_length=3, verbose_name='Status'),
        ),
    ]
