# Generated by Django 2.2.8 on 2020-02-14 06:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailkitcore', '0002_auto_20200210_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysettings',
            name='fiscal_year_start',
            field=models.DateField(default=datetime.datetime(2019, 12, 31, 17, 0, tzinfo=utc), verbose_name='Fiscal year start'),
        ),
    ]
