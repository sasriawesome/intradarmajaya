# Generated by Django 2.2.8 on 2020-01-19 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import uuid
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('reg_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('code', models.SlugField(max_length=256, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('teaching_method', models.CharField(max_length=256, verbose_name='Teaching method')),
                ('course_type', models.CharField(choices=[('A', 'Mandatory'), ('B', 'Choice'), ('C', 'Interest Mandatory'), ('D', 'Interest Choice'), ('S', 'Research/Thesis/Disertation')], default='A', max_length=1, verbose_name='Course type')),
                ('course_group', models.CharField(choices=[('A', 'MPK: Personal Development Course'), ('B', 'MKK: Knowledge Foudation Course'), ('C', 'MKB: Creational Skill Course'), ('D', 'MPB: Behavioral Skill Course'), ('E', 'MBB: Life Skill Course'), ('F', 'MKDU: Basic Knowledge Course'), ('G', 'MKDK: Basic Skill Course')], default='A', max_length=4, verbose_name='Course group')),
                ('description', wagtail.core.fields.RichTextField(blank=True, max_length=10000, null=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active status')),
                ('equal_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='academic.Course', verbose_name='Equal to')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('code', models.SlugField(max_length=256, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('sks_graduate', models.PositiveIntegerField(default=0, verbose_name='SKS graduate')),
            ],
            options={
                'verbose_name': 'Curriculum',
                'verbose_name_plural': 'Curriculums',
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('code', models.SlugField(max_length=256, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('date_start', models.DateField(verbose_name='Date start')),
                ('date_end', models.DateField(verbose_name='Date end')),
            ],
            options={
                'verbose_name': 'School Year',
                'verbose_name_plural': 'School Years',
            },
        ),
        migrations.CreateModel(
            name='ResourceManagementUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('code', models.SlugField(max_length=256, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academic.ResourceManagementUnit', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Resource Management Unit',
                'verbose_name_plural': 'Resource Management Unit',
            },
        ),
        migrations.CreateModel(
            name='ProgramStudy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('code', models.SlugField(max_length=256, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('alias', models.CharField(blank=True, max_length=512, null=True, verbose_name='Alias')),
                ('description', wagtail.core.fields.RichTextField(blank=True, max_length=10000, null=True, verbose_name='Description')),
                ('education_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='persons.EducationLevel', verbose_name='Level')),
                ('rmu', models.ForeignKey(help_text='Resource Management Unit', on_delete=django.db.models.deletion.PROTECT, to='academic.ResourceManagementUnit', verbose_name='RMU')),
            ],
            options={
                'verbose_name': 'Program Study',
                'verbose_name_plural': 'Program Studies',
            },
        ),
        migrations.CreateModel(
            name='CurriculumCourse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('reg_number', models.PositiveIntegerField(blank=True, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('sks', models.PositiveIntegerField(default=0, verbose_name='SKS')),
                ('sks_type', models.CharField(choices=[('M', 'Meeting'), ('P', 'Practice'), ('F', 'Field Practice'), ('S', 'Simulation')], default='M', max_length=1, verbose_name='SKS type')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Course', verbose_name='Course')),
                ('curricullum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.Curriculum', verbose_name='Curriculum')),
                ('rmu', models.ForeignKey(help_text='Resource Management Unit', on_delete=django.db.models.deletion.PROTECT, to='academic.ResourceManagementUnit', verbose_name='RMU')),
            ],
            options={
                'verbose_name': 'Curricullum Course',
                'verbose_name_plural': 'Curricullum Courses',
            },
        ),
        migrations.AddField(
            model_name='curriculum',
            name='prodi',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.ProgramStudy', verbose_name='Program Study'),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='rmu',
            field=models.ForeignKey(help_text='Resource Management Unit', on_delete=django.db.models.deletion.PROTECT, to='academic.ResourceManagementUnit', verbose_name='RMU'),
        ),
        migrations.CreateModel(
            name='CoursePreRequisite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date modified')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='course_prerequisites', to='academic.Course', verbose_name='Course')),
                ('requisite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='prerequisites', to='academic.Course', verbose_name='Requisite')),
            ],
            options={
                'verbose_name': 'Course Pre Requisite',
                'verbose_name_plural': 'Course Pre Requisite',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='rmu',
            field=models.ForeignKey(help_text='Resource Management Unit', on_delete=django.db.models.deletion.PROTECT, to='academic.ResourceManagementUnit', verbose_name='RMU'),
        ),
    ]
