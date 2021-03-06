# Generated by Django 2.2.10 on 2020-02-23 11:33

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0003_auto_20200223_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollmentitem',
            name='enrollment',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='enrollments.Enrollment', verbose_name='Enrolment'),
        ),
    ]
