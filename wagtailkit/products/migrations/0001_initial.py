# Generated by Django 2.2.10 on 2020-02-14 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import mptt.fields
import uuid
import wagtail.core.fields
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailimages', '0001_squashed_0021'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Delivery Method',
                'verbose_name_plural': 'Delivery Methods',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Payment Method',
                'verbose_name_plural': 'Payment Methods',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('barcode', models.CharField(blank=True, max_length=125, null=True, verbose_name='Barcode Number')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', wagtail.core.fields.RichTextField(blank=True, max_length=1000, null=True, verbose_name='Description')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=15, verbose_name='Unit price')),
                ('minimum_stock', models.PositiveIntegerField(default=10, verbose_name='Min stock')),
                ('maximum_stock', models.PositiveIntegerField(default=1000, verbose_name='Max stock')),
                ('is_locked', models.BooleanField(default=False, help_text='Lock to prevent unwanted editing', verbose_name='Locked')),
                ('is_active', models.BooleanField(default=True, help_text='Deletion is not good, set to inactive instead', verbose_name='Active')),
                ('is_consumable', models.BooleanField(default=True, help_text='This product is consumable', verbose_name='Consumable')),
                ('is_stockable', models.BooleanField(default=True, help_text='This product is stockable eg. inventory or asset types', verbose_name='Stockable')),
                ('is_bundle', models.BooleanField(default=False, help_text="This product's unit price and stock will ignored", verbose_name='Bundle')),
                ('is_sparepart', models.BooleanField(default=False, help_text='This product is sparepart item', verbose_name='Sparepart')),
                ('can_be_sold', models.BooleanField(default=False, verbose_name='Can be sold')),
                ('can_be_purchased', models.BooleanField(default=True, verbose_name='Can be purchased')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'permissions': (('lock_product', 'Can lock Product'), ('unlock_product', 'Can unlock Product'), ('export_product', 'Can export Product'), ('import_product', 'Can import Product')),
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Unit of measure',
                'verbose_name_plural': 'Unit of measures',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.Product')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
                'permissions': (('lock_asset', 'Can lock Asset'), ('unlock_asset', 'Can unlock Asset'), ('export_asset', 'Can export Asset'), ('import_asset', 'Can import Asset')),
            },
            bases=('products.product',),
        ),
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.Product')),
            ],
            options={
                'verbose_name': 'Bundle',
                'verbose_name_plural': 'Bundles',
                'permissions': (('lock_bundle', 'Can lock Bundle'), ('unlock_bundle', 'Can unlock Bundle'), ('export_bundle', 'Can export Bundle'), ('import_bundle', 'Can import Bundle')),
            },
            bases=('products.product',),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.Product')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventories',
                'permissions': (('lock_inventory', 'Can lock Inventory'), ('unlock_inventory', 'Can unlock Inventory'), ('export_inventory', 'Can export Inventory'), ('import_inventory', 'Can import Inventory')),
            },
            bases=('products.product',),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.Product')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'permissions': (('lock_service', 'Can lock Service'), ('unlock_service', 'Can unlock Service'), ('export_service', 'Can export Service'), ('import_service', 'Can import Service')),
            },
            bases=('products.product',),
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_products', to='products.Product')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_producttag_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductCategory', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.ProductCategory', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='creator',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='product',
            name='picture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='product',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_products.product_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='product',
            name='suppliers',
            field=models.ManyToManyField(blank=True, help_text='Product supplier or vendors', related_name='product_suppliers', to='partners.Supplier'),
        ),
        migrations.AddField(
            model_name='product',
            name='unit_of_measure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.UnitOfMeasure', verbose_name='Unit'),
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('feature', models.CharField(max_length=255, verbose_name='Feature')),
                ('value', models.CharField(max_length=255, verbose_name='Value')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='Note')),
                ('product', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_specifications', to='products.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Specification',
                'verbose_name_plural': 'Product Specifications',
                'unique_together': {('product', 'feature')},
            },
        ),
        migrations.CreateModel(
            name='Sparepart',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('sparepart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_spareparts', to='products.Product', verbose_name='Sparepart')),
                ('product', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='spareparts', to='products.Bundle', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Sparepart',
                'verbose_name_plural': 'Spareparts',
                'unique_together': {('product', 'sparepart')},
            },
        ),
    ]
