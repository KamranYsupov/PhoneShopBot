# Generated by Django 4.2.1 on 2025-04-04 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_settings', '0002_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='orders_receiver_telegram_id',
            field=models.BigIntegerField(default='6145206276', verbose_name='Телеграм ID'),
        ),
    ]
