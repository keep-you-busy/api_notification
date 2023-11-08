from django.contrib import admin

from users.models import Client, NewsLetter, Message
from users.forms import MessageFormSet


class MessageInline(admin.StackedInline):
    """Форма для модели Клиентов, связзаной по первичному ключу."""

    model = Message
    extra = 0
    formset = MessageFormSet


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Админ панель для модели Клиентов."""

    list_display = (
        'phone_number',
        'tag',
        'time_zone',
        'network_code',
    )
    readonly_fields = (
        'network_code',
    )
    search_fields = (
        'phone_number',
        'tag',
        'time_zone',
        'network_code',
    )
    empty_value_display = '-пусто-'


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    """Админ панель для модели Рассылок."""

    list_display = (
        'start_datetime',
        'text',
        'end_datetime',
    )
    search_fields = (
        'clients__time_zone',
        'clients__network_code',
    )
    list_filter = (
        'clients__time_zone',
        'clients__network_code',
    )
    empty_value_display = '-пусто-'
    inlines = (MessageInline,)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Админ панель для модели Сообщений."""

    search_fields = (
        'status',
        'newsletter',
        'client',
    )
    readonly_fields = (
        'get_start_newsletter',
        'status',
        'newsletter',
        'client',
    )
    empty_value_display = '-пусто-'

    def get_start_newsletter(self, message):
        return message.newsletter.start_datetime

    get_start_newsletter.short_description = 'Время запуска рассылки'
