# Generated by Django 2.2.8 on 2020-01-31 12:26

from django.db import migrations, models
from wagtailkit.warehouse.utils.migrations import (
    apply_create_wh_group, revert_create_wh_group,
    apply_create_wh_group_permissions, revert_create_wh_group_permissions
)


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            apply_create_wh_group,
            reverse_code=revert_create_wh_group),
        migrations.RunPython(
            apply_create_wh_group_permissions,
            reverse_code=revert_create_wh_group_permissions)
    ]