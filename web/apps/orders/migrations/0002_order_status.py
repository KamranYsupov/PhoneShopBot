# Generated by Django 4.2.1 on 2025-01-07 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ARRIVED', 'Прибыл'), ('BOUGHT', 'Куплен'), ('ASSEMBLED', 'Собран'), ('КNOCKED_OUT', 'Выбит'), ('CANCEL', 'Отменён')], default='ARRIVED', max_length=11),
        ),
    ]
