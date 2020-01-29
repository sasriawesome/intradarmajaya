# Generated by Django 2.2.8 on 2020-01-27 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0010_auto_20200127_0320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcemanagementunit',
            name='creator',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
    ]
