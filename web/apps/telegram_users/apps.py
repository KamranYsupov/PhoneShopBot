from django.apps import AppConfig


class TelegramUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web.apps.telegram_users'
    verbose_name = 'Управление пользователями'
