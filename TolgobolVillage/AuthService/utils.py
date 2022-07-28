from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy  as _
import re 

def validate_handle( field: str, format: set ):
    res = False
    for i in format:
        if re.search(i, field):
            res = True
    if not res:
        raise ValidationError( _(f'Не соответствует формату') )
    return field

def validate_telephon( telephon ):
    formats = (
        '^\+7\d\d\d\d\d\d\d\d\d\d$',
        '^\+7\(\d\d\d\)\d\d\d\d\d\d\d$',
        '^\+7\(\d\d\d\)\d\d\d-\d\d-\d\d$',
        '^8\d\d\d\d\d\d\d\d\d\d$',
        '^8\(\d\d\d\)\d\d\d\d\d\d\d$',
        '^8\(\d\d\d\)\d\d\d-\d\d-\d\d$',
    )
    tel = telephon
    tel = tel.replace( ' ', '' )
    return validate_handle( tel, formats )

def validate_email( email ):
    if not email: return None
    formats = (
        '.*@.*\..*',
    )
    return validate_handle( email, formats )