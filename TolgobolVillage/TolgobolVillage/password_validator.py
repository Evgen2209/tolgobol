
import gzip
import re
from difflib import SequenceMatcher
from pathlib import Path

from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _, ngettext

class MyMinimumLengthValidator:
    def __init__(self, min_length=0):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    _("Этот пароль слишком короткий. Он должен содержать не менее")+" %(min_length)d " + _("символов."),
                    _("Этот пароль слишком короткий. Он должен содержать не менее")+" %(min_length)d " + _("символов."),
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            _("Ваш пароль должен содержать по крайней мере") + " %(min_length)d " + _("символов."),
            _("Ваш пароль должен содержать по крайней мере") + " %(min_length)d " + _("символов."),
            self.min_length
        ) % {'min_length': self.min_length}


class MyUserAttributeSimilarityValidator:
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("Пароль слишком похож на %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _('Ваш пароль не может быть слишком похож на другую вашу личную информацию.')


class MyCommonPasswordValidator:
    DEFAULT_PASSWORD_LIST_PATH = Path(__file__).resolve().parent / 'common-passwords.txt.gz'

    def __init__(self, password_list_path=DEFAULT_PASSWORD_LIST_PATH):
        try:
            with gzip.open(password_list_path, 'rt', encoding='utf-8') as f:
                self.passwords = {x.strip() for x in f}
        except OSError:
            with open(password_list_path) as f:
                self.passwords = {x.strip() for x in f}

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("Этот пароль слишком распространен"),
                code='password_too_common',
            )

    def get_help_text(self):
        return _('Ваш пароль не может быть часто используемым паролем.')


class MyNumericPasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Этот пароль полностью из цифр"),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _('Ваш пароль не может быть полностью из цифр.')
