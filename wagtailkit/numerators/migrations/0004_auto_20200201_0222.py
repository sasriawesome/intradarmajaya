# Generated by Django 2.2.8 on 2020-01-31 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('numerators', '0003_auto_20200201_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numerator',
            name='dtype',
            field=models.CharField(max_length=50, verbose_name='Counter period'),
        ),
    ]
