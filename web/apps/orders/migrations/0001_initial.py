# Generated by Django 4.2.1 on 2025-01-07 13:43

from django.db import migrations, models
import django.db.models.deletion
import web.db.model_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('telegram_users', '0001_initial'),
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(db_index=True, default=web.db.model_mixins.ulid_default, editable=False, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('number', models.BigIntegerField(verbose_name='Номер заказа')),
                ('status', models.CharField(choices=[('ARRIVED', 'Прибыл'), ('BOUGHT', 'Куплен'), ('ASSEMBLED', 'Собран'), ('КNOCKED_OUT', 'Выбит'), ('CANCEL', 'Отменён')], default='ARRIVED', max_length=11, verbose_name='Статус')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='telegram_users.telegramuser', verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.CharField(db_index=True, default=web.db.model_mixins.ulid_default, editable=False, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.PositiveBigIntegerField(verbose_name='Количество')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='devices.device', verbose_name='Устройство')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
            options={
                'verbose_name': 'элемент заказа',
                'verbose_name_plural': 'элементы заказа',
            },
        ),
    ]