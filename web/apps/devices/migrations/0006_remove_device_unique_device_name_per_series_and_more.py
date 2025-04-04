# Generated by Django 4.2.1 on 2025-04-04 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_device_is_archived_devicecompany_is_archived_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='device',
            name='unique_device_name_per_series',
        ),
        migrations.RemoveConstraint(
            model_name='devicemodel',
            name='unique_model_name_per_company',
        ),
        migrations.RemoveConstraint(
            model_name='deviceseries',
            name='unique_series_name_per_model',
        ),
        migrations.AlterField(
            model_name='devicecompany',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Название'),
        ),
    ]
