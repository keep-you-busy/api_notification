from datetime import datetime
from requests import post
from requests.exceptions import RequestException

from celery import shared_task
from celery.utils.log import get_task_logger

from users.models import Message, NewsLetter, Client

token = 'ksk'
url = 'url'


logger = get_task_logger(__name__)


@shared_task(bind=True)
def send_message(self, message):
    client_time_zone = message.client.time_zone
    now_time = datetime.now(client_time_zone)
    if message.newsletter.start_datetime <= now_time <= message.newsletter.end_datetime:
        data = {
        'id': message.pk,
        'phone': message.client.phone_number,
        'text': message.newsletter.text,
        }   
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        try:
            post(url=url + str(message.pk), headers=header, json=data)
        except RequestException as error:
            logger.error(f'Ошибка в сообщении {message.pk}: {error}')
            raise self.retry(error)
        else:
            logger.info(f'Сообщение {message.pk}: Доставлено')
            message.update(status='ОТПРАВЛЕНО')
    else:
        time = 24 - (int(now_time.time().strftime('%H:%M:%S')[:2]) - int(message.newsletter.start_datetime.strftime('%H:%M:%S')[:2]))
        logger.info(
            f'Сообщение: {message.pk}, '
            f'Повторить через: {60 * 60 * time} сек'
        )
        return self.retry(countdown=60 * 60 * time)
