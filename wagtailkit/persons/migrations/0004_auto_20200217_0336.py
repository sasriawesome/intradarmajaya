# Generated by Django 2.2.10 on 2020-02-16 20:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0003_person_last_education_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='family',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='formaleducation',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='nonformaleducation',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='personaddress',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='working',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
    ]
