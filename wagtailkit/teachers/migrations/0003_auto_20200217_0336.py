# Generated by Django 2.2.10 on 2020-02-16 20:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_auto_20200215_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created'),
        ),
    ]
