# Generated by Django 2.2.8 on 2020-02-10 11:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailkitcore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysettings',
            name='fiscal_year_start',
            field=models.DateField(default=datetime.datetime(2020, 1, 1, 0, 0, tzinfo=utc), verbose_name='Fiscal year start'),
        ),
    ]
