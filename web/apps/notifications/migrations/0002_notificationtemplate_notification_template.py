# Generated by Django 4.2.1 on 2025-03-30 09:48

from django.db import migrations, models
import django.db.models.deletion
import web.db.model_mixins


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.CharField(db_index=True, default=web.db.model_mixins.ulid_default, editable=False, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, default=None, max_length=150, null=True, verbose_name='Название(опционально)')),
                ('text', models.TextField(max_length=4000, verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время и дата создания')),
            ],
            options={
                'verbose_name': 'Шаблон рассылки',
                'verbose_name_plural': 'Шаблоны рассылки',
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='template',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='notifications.notificationtemplate', verbose_name='Шаблон'),
        ),
    ]
