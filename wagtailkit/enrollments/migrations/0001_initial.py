# Generated by Django 2.2.10 on 2020-02-23 11:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid
import wagtailkit.enrollments.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lectures', '0001_initial'),
        ('academic', '0002_auto_20200217_0336'),
        ('students', '0004_student_coach'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Register number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('note', models.TextField(blank=True, max_length=256, null=True, verbose_name='Note for coach')),
                ('coach_review', models.TextField(blank=True, max_length=256, null=True, verbose_name='Coach review')),
                ('status', models.CharField(choices=[('TRASH', 'TRASH'), ('DRAFT', 'DRAFT'), ('SUBMITTED', 'SUBMITTED'), ('REVISION', 'REVISION'), ('VALID', 'VALID')], default=wagtailkit.enrollments.models.EnrollmentStatus('DRAFT'), max_length=2, verbose_name='Status')),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.AcademicYear', verbose_name='Academic Year')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Enrollment',
                'verbose_name_plural': 'Enrollments',
            },
        ),
        migrations.CreateModel(
            name='EnrolmentPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('criteria', models.CharField(choices=[('1', 'NEW'), ('2', 'REMEDY')], default=wagtailkit.enrollments.models.EnrollmentCriteria('1'), max_length=2, verbose_name='Criteria')),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lectures.Lecture', verbose_name='Lecture')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Enrollment Plan',
                'verbose_name_plural': 'Enrollment Plans',
            },
        ),
        migrations.CreateModel(
            name='EnrollmentItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date created')),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date modified')),
                ('is_deleted', models.BooleanField(default=False, editable=False)),
                ('criteria', models.CharField(choices=[('1', 'NEW'), ('2', 'REMEDY')], default=wagtailkit.enrollments.models.EnrollmentCriteria('1'), max_length=2, verbose_name='Criteria')),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enrollments.Enrollment', verbose_name='Enrolment')),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lectures.Lecture', verbose_name='Lecture')),
            ],
            options={
                'verbose_name': 'Enrollment Item',
                'verbose_name_plural': 'Enrollment Items',
                'unique_together': {('enrollment', 'lecture')},
            },
        ),
    ]
