# Generated by Django 2.2.10 on 2020-02-23 11:30

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0002_auto_20200223_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollmentitem',
            name='sort_order',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='enrollmentitem',
            name='enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='enrollments.Enrollment', verbose_name='Enrolment'),
        ),
        migrations.AlterField(
            model_name='enrollmentitem',
            name='lecture',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='lectures.Lecture', verbose_name='Lecture'),
        ),
    ]