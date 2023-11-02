from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField


class Client(models.Model):
    phone_number = PhoneNumberField(
        verbose_name='Номер телефона',
        unique=True,
        blank=False,
        region='RU')
    tag = models.CharField(
        verbose_name='Произвольная метка',
        max_length=50,
        blank=True
    )
    time_zone = TimeZoneField(
        verbose_name='Часовой пояс',
        default='Europe/Moscow',
    )

    @property
    def network_code(self):
        return self.phone_number.as_e164[2:5]

    def __str__(self) -> str:
        return f'[Client: {self.pk}; Number: {self.phone_number}]'


class NewsLetter(models.Model):
    start_datetime = models.DateTimeField(
        verbose_name='Время запуска рассылки',
        auto_created=True,
    )
    text = models.TextField(
        verbose_name='Текст сообщения',
    )
    client_operator_code = models.CharField(max_length=3)
    client_tag = models.CharField(max_length=50)
    end_datetime = models.DateTimeField(
        verbose_name='Время окончания рассылки',
        editable=True,
    )

    def __str__(self):
        return f'[Newsletter: {self.pk}; Start: {self.start_newsletter}]'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    SENT = "Отправлено"
    NO_SENT = "Не отправлено"

    STATUS_CHOICES = [
        (SENT, "Отправлено"),
        (NO_SENT, "Не отправлено"),
    ]

    start_newsletter = models.DateTimeField(
        verbose_name='Время запуска рассылки',
        auto_created=True,
    )
    status = models.BooleanField(
        verbose_name='Статус отправки',
        choices=STATUS_CHOICES
    )
    newsletter = models.ForeignKey(
        NewsLetter,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    def __str__(self):
        return f'[Message: {self.pk}; Status: {self.status}]'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
