# Generated by Django 4.2.1 on 2025-03-30 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notificationtemplate_notification_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=models.TextField(blank=True, default=None, max_length=4000, null=True, verbose_name='Текст'),
        ),
    ]
