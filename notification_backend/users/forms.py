from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class BaseNewsLetterFormSet(BaseInlineFormSet):
    """
    Базовый формсет для рассылки.

    Этот формсет обеспечивает валидацию элементов,
    гарантируя наличие хотя бы одного элемента.
    """

    def clean(self):
        """
        Пользовательский метод очистки формсета.

        Этот метод проверяет, что хотя бы один элемент указан в формсете.
        Если ни один элемент не указан, вызывается исключение ValidationError.
        """
        super().clean()
        has_at_least_one_item = False
        item_name = self.item_name

        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                item = form.cleaned_data.get(item_name)
                if item is None:
                    raise ValidationError('Обязательное поле.')
                has_at_least_one_item = True
        if not has_at_least_one_item:
            raise ValidationError(f'Необходимо хотя бы одно поле {item_name}.')


class MessageFormSet(BaseNewsLetterFormSet):
    """Формсет для клиентов в рассылках."""

    item_name = 'client'
