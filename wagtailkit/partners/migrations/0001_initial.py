# Generated by Django 2.2.10 on 2020-02-14 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'permissions': (('export_customer', 'Can export Customer'), ('import_customer', 'Can import Customer')),
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
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='persons.Person', verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
                'permissions': (('export_partner', 'Can export Partner'), ('import_partner', 'Can import Partner')),
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
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('partner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='partners.Partner', verbose_name='Partner')),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
                'permissions': (('export_supplier', 'Can export Supplier'), ('import_supplier', 'Can import Supplier')),
            },
        ),
        migrations.CreateModel(
            name='PartnerPersonal',
            fields=[
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
                'permissions': (('export_partnerpersonal', 'Can export Person Personal'), ('import_partnerpersonal', 'Can import Person Personal')),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('persons.person',),
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
                ('supplier', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_contactpersons', to='partners.Supplier', verbose_name='Supplier')),
            ],
            options={
                'verbose_name': 'Sales Persons',
                'verbose_name_plural': 'Sales Persons',
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
                ('partner', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, to='partners.Partner', verbose_name='Partner')),
            ],
            options={
                'verbose_name': 'Contact Info',
                'verbose_name_plural': 'Contact Info',
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
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('partner', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, to='partners.Partner', verbose_name='Partner')),
            ],
            options={
                'verbose_name': 'Billing Address',
                'verbose_name_plural': 'Billing Address',
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
                ('customer', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_contactpersons', to='partners.Customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Contact Person',
                'verbose_name_plural': 'Contact Persons',
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='partner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='partners.Partner', verbose_name='Partner'),
        ),
    ]
