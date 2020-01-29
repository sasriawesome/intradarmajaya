# Generated by Django 2.2.8 on 2020-01-27 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0013_auto_20200127_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='has_lpu',
            field=models.BooleanField(default=True, help_text='Lecture Program Unit a.k.a SAP', verbose_name='Has LPU'),
        ),
    ]
