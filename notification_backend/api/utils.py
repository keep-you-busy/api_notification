from users.models import NewsLetter


def set_clients_values(newsletter: NewsLetter, value_name: str):
    """Возвращает множество значений Клиента."""
    newsletter_values = newsletter.clients.values(value_name)
    values_set = set(item[value_name] for item in newsletter_values)
    return values_set
