# Generated by Django 2.2.8 on 2020-01-29 21:20

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintPDFSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index_orientation', models.CharField(choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')], default='portrait', help_text='Document orientation', max_length=50, verbose_name='Orientation')),
                ('index_paper_size', models.CharField(choices=[('A4', 'A4'), ('folio', 'Folio')], default='A4', help_text='Set document paper size', max_length=50, verbose_name='Paper size')),
                ('index_show_cover', models.BooleanField(default=False, help_text='Show document cover', verbose_name='Show cover')),
                ('index_show_header', models.BooleanField(default=True, help_text='Show document header', verbose_name='Show header')),
                ('index_show_footer', models.BooleanField(default=True, help_text='Show document footer', verbose_name='Show footer')),
                ('index_margin_top', models.IntegerField(default=45, help_text='Set index document top margin', verbose_name='Top')),
                ('index_margin_bottom', models.IntegerField(default=25, help_text='Set index document bottom margin', verbose_name='Bottom')),
                ('index_margin_left', models.IntegerField(default=25, help_text='Set index document left margin', verbose_name='Left')),
                ('index_margin_right', models.IntegerField(default=25, help_text='Set index document right margin', verbose_name='Right')),
                ('detail_orientation', models.CharField(choices=[('portrait', 'Portrait'), ('landscape', 'Landscape')], default='portrait', help_text='Document orientation', max_length=50, verbose_name='Orientation')),
                ('detail_paper_size', models.CharField(choices=[('A4', 'A4'), ('folio', 'Folio')], default='A4', help_text='Set document paper size', max_length=50, verbose_name='Paper size')),
                ('detail_show_cover', models.BooleanField(default=True, help_text='Show document cover', verbose_name='Show cover')),
                ('detail_show_header', models.BooleanField(default=True, help_text='Show document header', verbose_name='Show header')),
                ('detail_show_footer', models.BooleanField(default=True, help_text='Show document footer', verbose_name='Show footer')),
                ('detail_margin_top', models.IntegerField(default=45, help_text='Set index document top margin', verbose_name='Top')),
                ('detail_margin_bottom', models.IntegerField(default=25, help_text='Set index document bottom margin', verbose_name='Bottom')),
                ('detail_margin_left', models.IntegerField(default=25, help_text='Set index document left margin', verbose_name='Left')),
                ('detail_margin_right', models.IntegerField(default=25, help_text='Set index document right margin', verbose_name='Right')),
                ('custom_css', models.TextField(blank=True, help_text='Add custom style to PDF', max_length=2000, null=True, verbose_name='Custom CSS')),
                ('content_cover', wagtail.core.fields.RichTextField(blank=True, default='\n<h1>Awesome Company</h1>\n<p>Made with taste<p/>\n', help_text='Insert HTML content to document cover, use Custom CSS for better display', max_length=2000, null=True, verbose_name='Cover content')),
                ('content_header', wagtail.core.fields.RichTextField(blank=True, default='\n    <h1>Awesome Company</h1>\n    <p>Made with taste<p/>\n', help_text='Insert HTML content to document header, use Custom CSS for better display', max_length=2000, null=True, verbose_name='Header content')),
                ('content_footer', wagtail.core.fields.RichTextField(blank=True, default='\n    <p>Feel free to contact 24/7 always on.<p/>\n', help_text='Insert HTML content to document footer, use Custom CSS for better display', max_length=2000, null=True, verbose_name='Header content')),
                ('site', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='wagtailcore.Site')),
            ],
            options={
                'verbose_name': 'PDF Print',
            },
        ),
    ]