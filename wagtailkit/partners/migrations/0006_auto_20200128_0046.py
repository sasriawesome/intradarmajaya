# Generated by Django 2.2.8 on 2020-01-27 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0005_auto_20200127_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='inner_id',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='inner_id',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='inner_id',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID'),
        ),
    ]
