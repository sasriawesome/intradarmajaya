# Generated by Django 2.2.8 on 2020-02-14 06:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import modelcluster.fields
import mptt.fields
import uuid
import wagtail.core.fields
import wagtail.search.index
import wagtailkit.warehouse.models.transfer


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailimages', '0001_squashed_0021'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTransfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('status', models.CharField(choices=[('trash', 'Trash'), ('draft', 'Draft'), ('valid', 'Valid'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('process', 'Process'), ('complete', 'Complete'), ('closed', 'Closed')], default='draft', editable=False, max_length=15, verbose_name='Status')),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('reftype', models.CharField(choices=[('IN', 'Check in'), ('OUT', 'Check out')], default='IN', max_length=3, verbose_name='Transfer')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_warehouse.producttransfer_set+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Transfer',
                'verbose_name_plural': 'Transfers',
                'permissions': (('trash_producttransfer', 'Can trash Product Transfer'), ('draft_producttransfer', 'Can draft Product Transfer'), ('validate_producttransfer', 'Can validate Product Transfer'), ('process_producttransfer', 'Can process Product Transfer'), ('complete_producttransfer', 'Can complete Product Transfer'), ('print_producttransfer', 'Can complete Product Transfer')),
            },
        ),
        migrations.CreateModel(
            name='TransferCheckIn',
            fields=[
                ('producttransfer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='warehouse.ProductTransfer')),
                ('reference', models.CharField(max_length=256, verbose_name='Reference')),
                ('sender', models.CharField(max_length=256, verbose_name='Sender')),
                ('department', models.CharField(max_length=256, verbose_name='Department')),
                ('received_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date received')),
            ],
            options={
                'verbose_name': 'Check In',
                'verbose_name_plural': 'Check Ins',
                'permissions': (('trash_transfercheckin', 'Can trash Transfer Check In'), ('draft_transfercheckin', 'Can draft Transfer Check In'), ('validate_transfercheckin', 'Can validate Transfer Check In'), ('process_transfercheckin', 'Can process Transfer Check In'), ('complete_transfercheckin', 'Can complete Transfer Check In'), ('print_transfercheckin', 'Can complete Transfer Check In')),
            },
            bases=('warehouse.producttransfer',),
        ),
        migrations.CreateModel(
            name='WarehouseLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128, verbose_name='Code')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('loc_type', models.CharField(choices=[('PSC', 'Physical'), ('VRT', 'Virtual')], default='PSC', max_length=128, verbose_name='Location type')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.WarehouseLocation', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
            bases=(wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='StockCard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('stock_on_hand', models.PositiveIntegerField(default=0, verbose_name='On hand')),
                ('stock_on_request', models.PositiveIntegerField(default=0, verbose_name='On request')),
                ('stock_on_delivery', models.PositiveIntegerField(default=0, verbose_name='On delivery')),
                ('stock_scrapped', models.PositiveIntegerField(default=0, verbose_name='Scrapped')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Stock Card',
                'verbose_name_plural': 'Stock Cards',
            },
        ),
        migrations.CreateModel(
            name='StockAdjustment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
                ('effective_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Effective date')),
                ('is_valid', models.BooleanField(default=False, verbose_name='Validated')),
                ('is_reconciled', models.BooleanField(default=False, verbose_name='Reconciled')),
                ('date_reconciled', models.DateTimeField(blank=True, null=True, verbose_name='Reconciled date')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('reconciled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inventoryadjustment_reconciled_by', to=settings.AUTH_USER_MODEL, verbose_name='Reconciled by')),
            ],
            options={
                'verbose_name': 'Stock Adjustment',
                'verbose_name_plural': 'Stock Adjustments',
                'permissions': (('validate_stockadjustment', 'Can validate Stock Adjustment'), ('reconcile_stockadjustment', 'Can reconcile Stock Adjustment'), ('print_stockadjustment', 'Can print Stock Adjustment'), ('edit_other_stockadjustment', 'Can edit other Stock Adjustment')),
            },
        ),
        migrations.CreateModel(
            name='RequestOrder',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('status', models.CharField(choices=[('trash', 'Trash'), ('draft', 'Draft'), ('valid', 'Valid'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('process', 'Process'), ('complete', 'Complete'), ('closed', 'Closed')], default='draft', editable=False, max_length=15, verbose_name='Status')),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('deliver_to', models.CharField(max_length=256, verbose_name='Deliver to')),
                ('title', models.CharField(max_length=512, verbose_name='Purpose of use')),
                ('description', wagtail.core.fields.RichTextField(default='\n        <p>Mohon dipenuhi permintaan persediaan dan asset berikut ini.<p/>\n        <p><strong>Terima Kasih</strong></p>\n        ', max_length=10000, verbose_name='Description')),
                ('rejection_note', wagtail.core.fields.RichTextField(blank=True, max_length=10000, null=True, verbose_name='Rejection note')),
                ('critical_status', models.CharField(choices=[('NRM', 'Normal'), ('URG', 'Urgent'), ('CRT', 'Critical')], default='NRM', max_length=3, verbose_name='Status')),
                ('deadline', models.DateTimeField(default=django.utils.timezone.now, verbose_name='On Deadline')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('department', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='department_wh_requests', to='organizations.Department', verbose_name='Department')),
                ('requester', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='position_wh_requests', to='organizations.Position', verbose_name='Requester')),
            ],
            options={
                'verbose_name': 'Request Order',
                'verbose_name_plural': 'Request Orders',
                'ordering': ['-date_created'],
                'permissions': (('trash_requestorder', 'Can trash Request Order'), ('draft_requestorder', 'Can draft Request Order'), ('validate_requestorder', 'Can validate Request Order'), ('approve_requestorder', 'Can approve Request Order'), ('reject_requestorder', 'Can reject Request Order'), ('process_requestorder', 'Can process Request Order'), ('complete_requestorder', 'Can complete Request Order'), ('close_requestorder', 'Can close Request Order'), ('print_requestorder', 'Can print Request Order'), ('changeother_requestorder', 'Can change other Request Order'), ('viewother_requestorder', 'Can view other Request Order')),
                'index_together': {('date_created', 'creator')},
            },
        ),
        migrations.CreateModel(
            name='ProductStorage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('name', models.CharField(max_length=256, verbose_name='Storage name')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.WarehouseLocation', verbose_name='Location')),
                ('products', models.ManyToManyField(related_name='storage_location', to='products.Product', verbose_name='Products')),
            ],
            options={
                'verbose_name': 'Product Storage',
                'verbose_name_plural': 'Product Storages',
            },
        ),
        migrations.CreateModel(
            name='NewProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('quantity_requested', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('quantity_approved', models.PositiveIntegerField(default=0, verbose_name='Approved Quantity')),
                ('description', wagtail.core.fields.RichTextField(blank=True, max_length=1000, null=True, verbose_name='Description')),
                ('category', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='products.ProductCategory', verbose_name='Category')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('picture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image')),
                ('request', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_new_products', to='warehouse.RequestOrder', verbose_name='Request Order')),
            ],
            options={
                'verbose_name': 'New Product',
                'verbose_name_plural': 'New Products',
            },
        ),
        migrations.CreateModel(
            name='TransferScrapped',
            fields=[
                ('producttransfer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='warehouse.ProductTransfer')),
                ('remover', models.CharField(max_length=256, verbose_name='Remover')),
                ('reference', models.CharField(max_length=256, verbose_name='Reference')),
                ('scrapped_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date scrapped')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='warehouse.WarehouseLocation', verbose_name='Location')),
            ],
            options={
                'verbose_name': 'Scrapped',
                'verbose_name_plural': 'Scrappeds',
                'permissions': (('trash_transferscrapped', 'Can trash Transfer Scrapped'), ('draft_transferscrapped', 'Can draft Transfer Scrapped'), ('validate_transferscrapped', 'Can validate Transfer Scrapped'), ('process_transferscrapped', 'Can process Transfer Scrapped'), ('complete_transferscrapped', 'Can complete Transfer Scrapped'), ('print_transferscrapped', 'Can complete Transfer Scrapped')),
            },
            bases=('warehouse.producttransfer',),
        ),
        migrations.CreateModel(
            name='TransferCheckOut',
            fields=[
                ('producttransfer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='warehouse.ProductTransfer')),
                ('requester', models.CharField(max_length=256, verbose_name='Requester')),
                ('department', models.CharField(max_length=256, verbose_name='Department')),
                ('deliver_to', models.CharField(max_length=256, verbose_name='Deliver to')),
                ('delivered_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date delivered')),
                ('request_order', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='warehouse.RequestOrder', verbose_name='Request Order')),
            ],
            options={
                'verbose_name': 'Check Out',
                'verbose_name_plural': 'Check Outs',
                'ordering': ['-date_created'],
                'permissions': (('trash_transfercheckout', 'Can trash Transfer Check Out'), ('draft_transfercheckout', 'Can draft Transfer Check Out'), ('validate_transfercheckout', 'Can validate Transfer Check Out'), ('process_transfercheckout', 'Can process Transfer Check Out'), ('complete_transfercheckout', 'Can complete Transfer Check Out'), ('print_transfercheckout', 'Can complete Transfer Check Out')),
            },
            bases=('warehouse.producttransfer',),
        ),
        migrations.CreateModel(
            name='InventoryTransferLine',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Minimum value is 1'), django.core.validators.MaxValueValidator(1000, message='Maximum value is 1000')], verbose_name='Quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Inventory', verbose_name='Product')),
                ('producttransfer', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_transfers', to='warehouse.ProductTransfer', verbose_name='Product transfer')),
            ],
            options={
                'verbose_name': 'Inventory Check In',
                'verbose_name_plural': 'Inventory Check Ins',
                'unique_together': {('producttransfer', 'product')},
            },
            bases=(wagtailkit.warehouse.models.transfer.TransferLineValidation, models.Model),
        ),
        migrations.CreateModel(
            name='InventoryRequestItem',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('quantity_requested', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Minimum value is 1'), django.core.validators.MaxValueValidator(1000, message='Maximum value is 1000')], verbose_name='Quantity')),
                ('quantity_approved', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='Minimum value is 0'), django.core.validators.MaxValueValidator(1000, message='Maximum value is 1000')], verbose_name='Approved quantity')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Inventory', verbose_name='Product')),
                ('request_order', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_inventories', to='warehouse.RequestOrder', verbose_name='Request order')),
            ],
            options={
                'verbose_name': 'Inventory Request Item',
                'verbose_name_plural': 'Inventory Request Item',
                'unique_together': {('request_order', 'product')},
            },
        ),
        migrations.CreateModel(
            name='AssetTransferLine',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Minimum value is 1'), django.core.validators.MaxValueValidator(1000, message='Maximum value is 1000')], verbose_name='Quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Asset', verbose_name='Product')),
                ('producttransfer', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_transfers', to='warehouse.ProductTransfer', verbose_name='Product transfer')),
            ],
            options={
                'verbose_name': 'Asset Transfer',
                'verbose_name_plural': 'Asset Transfers',
                'unique_together': {('producttransfer', 'product')},
            },
            bases=(wagtailkit.warehouse.models.transfer.TransferLineValidation, models.Model),
        ),
        migrations.CreateModel(
            name='AssetRequestItem',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('quantity_requested', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Minimum value is 1'), django.core.validators.MaxValueValidator(1000, message='Maximum value is 1000')], verbose_name='Quantity')),
                ('quantity_approved', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='Minimum value is 0'), django.core.validators.MaxValueValidator(1000, message='Maximum value is 1000')], verbose_name='Approved quantity')),
                ('creator', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.Asset', verbose_name='Product')),
                ('request_order', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_assets', to='warehouse.RequestOrder', verbose_name='Request order')),
            ],
            options={
                'verbose_name': 'Asset Request Item',
                'verbose_name_plural': 'Asset Request Item',
                'unique_together': {('request_order', 'product')},
            },
        ),
        migrations.CreateModel(
            name='AdjustedProduct',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('stock_on_hand', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('stock_scrapped', models.PositiveIntegerField(default=0, verbose_name='Scrapped')),
                ('new_stock_on_hand', models.PositiveIntegerField(default=0, verbose_name='New Stock')),
                ('new_stock_scrapped', models.PositiveIntegerField(default=0, verbose_name='New Scrapped')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='Product')),
                ('stock_adjustment', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjusted_products', to='warehouse.StockAdjustment', verbose_name='Stock Adjustment')),
            ],
            options={
                'verbose_name': 'Adjusted Product',
                'verbose_name_plural': 'Adjusted Products',
                'unique_together': {('stock_adjustment', 'product')},
                'index_together': {('stock_adjustment', 'product')},
            },
        ),
    ]