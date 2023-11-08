from django.db import models
from timezone_field import TimeZoneField
from django.core.validators import RegexValidator


class Client(models.Model):
    phone_regex = RegexValidator(
                regex=r'^7\d{10}$',
            )
    phone_number = models.CharField(
        verbose_name='Телефон',
        validators=[
            phone_regex
        ],
        unique=True,
        max_length=11)
    tag = models.CharField(
        verbose_name='Произвольная метка',
        max_length=50,
        blank=True
    )
    network_code = models.CharField(
        verbose_name='Код оператора',
        max_length=3,
        blank=True
    )
    time_zone = TimeZoneField(
        verbose_name='Часовой пояс',
        default='Europe/Moscow',
    )

    def save(self, *args, **kwargs):
        self.network_code = self.phone_number[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Клиент ID: {self.pk}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class NewsLetter(models.Model):
    start_datetime = models.DateTimeField(
        verbose_name='Время запуска рассылки',
        auto_created=True,
    )
    text = models.TextField(
        verbose_name='Текст сообщения',
    )
    clients = models.ManyToManyField(
        Client,
        through='Message',
        verbose_name='Клиенты рассылки',
        related_name='newsletters',
    )
    end_datetime = models.DateTimeField(
        verbose_name='Время окончания рассылки',
        editable=True,
    )

    def __str__(self):
        return f'Рассылка ID: {self.pk}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    SENT = 'ОТПРАВЛЕНО'
    NOT_SENT = 'НЕ ОТПРАВЛЕНО'

    STATUS_CHOICES = [
        (SENT, 'Отправлено'),
        (NOT_SENT, 'Не отправлено'),
    ]

    status = models.CharField(
        verbose_name='Статус отправки',
        choices=STATUS_CHOICES,
        default=NOT_SENT,
    )
    newsletter = models.ForeignKey(
        NewsLetter,
        verbose_name='Рассылка',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        on_delete=models.CASCADE,
        related_name='messages'
    )

    def get_start_newsletter(self):
        return self.newsletter.start_datetime

    def __str__(self) -> str:
        return f'{self.client}; {self.status}; {self.newsletter}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
