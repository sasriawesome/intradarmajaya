# Generated by Django 2.2.8 on 2020-02-08 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtaildocs', '0010_document_file_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('code', models.CharField(max_length=256, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_upline', to='organizations.Department', verbose_name='Upline')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('is_manager', models.BooleanField(default=False, verbose_name='Is Manager')),
                ('is_co_manager', models.BooleanField(default=False, verbose_name='Is Co-Manager')),
                ('employee_required', models.IntegerField(default=1, verbose_name='Employee required')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('attachment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.Document')),
                ('department', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='staffs', to='organizations.Department', verbose_name='Department')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chair_upline', to='organizations.Position', verbose_name='Upline')),
            ],
            options={
                'verbose_name': 'Chair',
                'verbose_name_plural': 'Chairs',
            },
        ),
    ]
