# Generated by Django 2.2.10 on 2020-02-16 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20200216_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='last_education_institution',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Institution'),
        ),
    ]
