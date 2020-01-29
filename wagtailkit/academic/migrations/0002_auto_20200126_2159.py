# Generated by Django 2.2.8 on 2020-01-26 14:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('code', models.CharField(max_length=256, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('alias', models.CharField(blank=True, max_length=512, null=True, verbose_name='Alias')),
            ],
            options={
                'verbose_name': 'Course Group',
                'verbose_name_plural': 'Course Groups',
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('code', models.CharField(max_length=256, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('alias', models.CharField(blank=True, max_length=512, null=True, verbose_name='Alias')),
            ],
            options={
                'verbose_name': 'Course Type',
                'verbose_name_plural': 'Course Types',
            },
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name': 'Faculty', 'verbose_name_plural': 'Faculties'},
        ),
        migrations.AlterField(
            model_name='course',
            name='course_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.CourseGroup', verbose_name='Course group'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.CourseType', verbose_name='Course type'),
        ),
        migrations.AlterField(
            model_name='programstudy',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.Faculty', verbose_name='Faculty'),
        ),
        migrations.AlterField(
            model_name='programstudy',
            name='level',
            field=models.CharField(choices=[('3', 'D3'), ('1', 'S1'), ('2', 'S2'), ('4', 'S3')], default='1', max_length=3, verbose_name='Level'),
        ),
    ]
