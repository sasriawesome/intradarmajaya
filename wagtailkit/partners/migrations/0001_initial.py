# Generated by Django 2.2.8 on 2020-02-14 06:03

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'permissions': (('export_customer', 'Can export Customer'), ('import_customer', 'Can import Customer')),
            },
        ),
        migrations.CreateModel(
            name='CustomerContactPerson',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('department', models.CharField(blank=True, max_length=255, null=True, verbose_name='Department')),
            ],
            options={
                'verbose_name': 'Contact Person',
                'verbose_name_plural': 'Contact Persons',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('name', models.CharField(help_text='Partner name eg. Google .Inc or person name if partner is personal', max_length=255, verbose_name='Partner name')),
                ('is_company', models.BooleanField(default=True, verbose_name='Company')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('date_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Created date')),
            ],
            options={
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
                'permissions': (('export_partner', 'Can export Partner'), ('import_partner', 'Can import Partner')),
            },
        ),
        migrations.CreateModel(
            name='PartnerAddress',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('street1', models.CharField(blank=True, max_length=512, null=True, verbose_name='Address 1')),
                ('street2', models.CharField(blank=True, max_length=512, null=True, verbose_name='Address 2')),
                ('city', models.CharField(blank=True, max_length=128, null=True, verbose_name='City')),
                ('province', models.CharField(blank=True, max_length=128, null=True, verbose_name='Province')),
                ('country', models.CharField(blank=True, max_length=128, null=True, verbose_name='Country')),
                ('zipcode', models.CharField(blank=True, max_length=128, null=True, verbose_name='Zip Code')),
                ('is_primary', models.BooleanField(default=True, verbose_name='Primary')),
                ('name', models.CharField(help_text='E.g. Shipping or Billing Address', max_length=255, null=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Billing Address',
                'verbose_name_plural': 'Billing Address',
            },
        ),
        migrations.CreateModel(
            name='PartnerContactInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('phone1', models.CharField(blank=True, max_length=128, null=True, verbose_name='Phone 1')),
                ('fax', models.CharField(blank=True, max_length=128, null=True, verbose_name='Fax')),
                ('whatsapp', models.CharField(blank=True, max_length=128, null=True, verbose_name='Whatsapp')),
                ('email', models.EmailField(blank=True, max_length=128, null=True, verbose_name='Email')),
                ('website', models.CharField(blank=True, max_length=128, null=True, verbose_name='Website')),
            ],
            options={
                'verbose_name': 'Contact Info',
                'verbose_name_plural': 'Contact Info',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
                'permissions': (('export_supplier', 'Can export Supplier'), ('import_supplier', 'Can import Supplier')),
            },
        ),
        migrations.CreateModel(
            name='SupplierContactPerson',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone', models.CharField(max_length=255, verbose_name='Phone')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('department', models.CharField(blank=True, max_length=255, null=True, verbose_name='Department')),
            ],
            options={
                'verbose_name': 'Sales Persons',
                'verbose_name_plural': 'Sales Persons',
            },
        ),
    ]