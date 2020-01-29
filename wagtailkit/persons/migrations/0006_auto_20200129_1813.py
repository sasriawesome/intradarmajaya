# Generated by Django 2.2.8 on 2020-01-29 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0005_auto_20200128_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='phone2',
        ),
        migrations.AddField(
            model_name='person',
            name='fax',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Fax'),
        ),
        migrations.AddField(
            model_name='person',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Whatsapp'),
        ),
    ]
