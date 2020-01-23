# Generated by Django 2.2.8 on 2020-01-15 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportExportSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('export_csv', models.BooleanField(default=True, verbose_name='Export as CSV file')),
                ('export_xls', models.BooleanField(default=True, verbose_name='Export as XLS file')),
                ('export_xlsx', models.BooleanField(default=True, verbose_name='Export as XLSX file')),
                ('export_json', models.BooleanField(default=True, verbose_name='Export as JSON file')),
                ('import_csv', models.BooleanField(default=True, verbose_name='Import as CSV file')),
                ('import_xls', models.BooleanField(default=True, verbose_name='Import as XLS file')),
                ('import_xlsx', models.BooleanField(default=True, verbose_name='Import as XLSX file')),
                ('import_json', models.BooleanField(default=True, verbose_name='Import as JSON file')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'Import Export',
                'verbose_name_plural': 'Import Exports',
            },
        ),
    ]
