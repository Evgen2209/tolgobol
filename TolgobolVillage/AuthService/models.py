from django.db import models
from django.contrib.auth.models import AbstractUser, Group, GroupManager
from django.contrib.auth import validators
from django.utils.translation import gettext_lazy as _
import uuid
import secrets

class Strit( models.Model ):
    strit_name = models.CharField( _('Название Улицы'), max_length=200, blank=False, unique=True )

class Adres( models.Model ):
    strit = models.ForeignKey( Strit, on_delete = models.CASCADE )
    hous = models.CharField( _('Номер Дома'), max_length=15, blank=False )
    kv = models.CharField( _('Номер квартиры'), max_length=3, blank=True, null=True )
    
    def get_adres( self ):
        kv = '/'+self.kv if self.kv else ''
        return self.hous + kv
    def __str__(self ):
        return f'{self.strit.strit_name} {self.hous}' + ('' if not self.kv else f'/{self.kv}')

class User( AbstractUser ):
    user_id = models.UUIDField( default=uuid.uuid4, editable=False, unique=True )
    

    username_validator = validators.UnicodeUsernameValidator()
    password = models.CharField( _('Пароль'), max_length=128 )
    username = models.CharField(
        _('Логин'),
        blank=False,
        max_length=150,
        unique=True,
        help_text=_('Требования. не менее 6 символов. Только буквы, цифры и символы @/./+/-/_ '),
        validators=[username_validator],
        error_messages={
            'unique': _("Пользователь с таким логином уже существует."),
        },
    )
    adres =  models.ForeignKey( Adres, on_delete = models.CASCADE, blank=False )
    first_name = models.CharField( _('Имя'), max_length=150, blank=False )
    last_name = models.CharField( _('Фамилия'), max_length=150, blank=True )
    patronymic = models.CharField( _('Отчество'), max_length=150, blank=True )
    telephon = models.CharField( max_length=12, blank=True )
    email = models.EmailField( _('Email адрес'), blank=True, null=True )
    male = models.CharField( _('Пол'), max_length=150, blank=False )
    birthday = models.DateField( _('День рождения'), blank=True, null=True )
    is_starosta = models.BooleanField( _('Является ли старостой'), default=False ) 
    is_active = models.BooleanField( 
        _('Подтвержден'),
        default=True,
        help_text=_(
            'Поле говорит о том аккаунт подтвержден'
            'Снимите этот флаг вместо удаления аккаунта'
        ),
    )
    # токен для подтверждения аккаунта
    token = models.CharField( max_length=120, blank=True, default=secrets.token_urlsafe, editable=False, )

    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )

    def __str__(self) -> str:
        return '{} {}'.format( self.first_name, self.last_name )
    
    def is_fond_manager( self ):
        return self.groups.filter(id=1).count()