from datetime import datetime
from requests import post
from requests.exceptions import RequestException

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings


logger = get_task_logger(__name__)


@shared_task(bind=True, autoretry_for=(RequestException,), retry_backoff=True, serializer='pickle')
def send_message(self, message):
    client_now_time = datetime.now(message.client.time_zone)
    if message.newsletter.start_datetime <= client_now_time <= message.newsletter.end_datetime:
        data = {
            'id': message.pk,
            'phone': message.client.phone_number,
            'text': message.newsletter.text,
        }
        header = {
            'Authorization': f'Bearer {settings.PROBE_TOKEN}',
            'Content-Type': 'application/json',
        }
        try:
            response = post(url=settings.PROBE_URL + str(message.pk),
                            headers=header, json=data)
            response.raise_for_status()
        except RequestException as error:
            logger.error(f'Ошибка в сообщении {message.pk}: {error}')
        else:
            logger.info(f'Сообщение {message.pk}: Отправлено')
            message.status = 'ОТПРАВЛЕНО'
            message.save(update_fields=['status'])
