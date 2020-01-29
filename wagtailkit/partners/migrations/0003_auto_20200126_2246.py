# Generated by Django 2.2.8 on 2020-01-26 15:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0002_auto_20200115_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='date_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified'),
        ),
        migrations.AlterField(
            model_name='customercontactperson',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='customercontactperson',
            name='date_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='date_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified'),
        ),
        migrations.AlterField(
            model_name='partneraddress',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='partneraddress',
            name='date_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='date_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified'),
        ),
        migrations.AlterField(
            model_name='suppliercontactperson',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created'),
        ),
        migrations.AlterField(
            model_name='suppliercontactperson',
            name='date_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified'),
        ),
    ]
