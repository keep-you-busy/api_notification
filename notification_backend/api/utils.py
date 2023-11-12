from users.models import NewsLetter, Client


def set_clients_values(newsletter: NewsLetter, value_name: str):
    """Возвращает множество значений Клиента."""
    newsletter_values = newsletter.clients.values(value_name)
    values_set = set(item[value_name] for item in newsletter_values)
    return values_set


def update_or_create_newsletter(validated_data, instance=None):
    """Обновляет или создает объект Рассылки."""
    tags = validated_data.pop('tags')
    network_codes = validated_data.pop('network_codes')
    clients = Client.objects.filter(
            tag__in=tags,
            network_code__in=network_codes)
    if instance:
        instance.start_datetime = validated_data.get(
            'start_datetime', instance.start_datetime
        )
        instance.end_datetime = validated_data.get(
            'end_datetime', instance.end_datetime
        )
        instance.text = validated_data.get(
            'text', instance.text
        )
        instance.clients.clear()
    else:
        instance = NewsLetter.objects.create(**validated_data)
    instance.clients.set(clients)

    return instance


def retrieve_messages_statistic(messsages):
    """Возвращает статистику по сообщениям."""
    total_messages = messsages.count()
    recieved_messages = messsages.filter(
        status='ОТПРАВЛЕНО').count()
    awaiting_messages = messsages.filter(
        status='НЕ ОТПРАВЛЕНО').count()
    response = {
        'total messages': total_messages,
        'recieved messages': recieved_messages,
        'awaiting messages': awaiting_messages,
    }

    return response
