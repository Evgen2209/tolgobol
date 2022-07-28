from django.utils.translation import gettext_lazy  as _

from AuthService.forms import AuthLoginForm
from MainService.models import *
MENU = [
    { 'title':_('Главная'), 'url_name':'home' },
    { 'title':_('Важное'), 'url_name':'important', 'sub_menu': ({'sub_title': _('Контакты'), 'url_name': 'important'}, 
                                                               {'sub_title': _('Голосование'), 'url_name': 'important'}) },
    { 'title':_('Обсуждение'), 'url_name':'forum' },
    { 'title':_('Сборы'), 'url_name':'collection', 'sub_menu': ({'sub_title': _('Цели'), 'url_name': 'collection'},
                                                                {'sub_title': _('Траты'), 'url_name': 'collection'}) },
]
    
AUTH_MENU = {
    'auth': { 'title':_('Кабинет'), 'url_name':'account' },
    'anonymous': { 'title':_('Войти'), 'url_name':'login' },
}

ACCOUNT_MENU = [
    { 'title': _('Профиль'), 'url_name':'person' },
    { 'title': _('Заказы'), 'url_name':'orders' },
    { 'title': _('История заказов'), 'url_name':'history' },
    { 'title': _('Адреса доставки'), 'url_name':'address' },
    { 'title': _('Выйти'), 'url_name':'logout' }
]

class DataMixin:
    def get_user_context( self, **kwargs ):
        context = kwargs
        user_menu = MENU.copy()
        if self.request.user.is_authenticated:
            context[ 'account' ] = { 'title': self.request.user.first_name, 
                                    'url_name':'account',
                                    'sub_menu': (
                                        {'sub_title': _('Личный кабинет'), 'url_name': 'account'},
                                        {'sub_title': _('Изменить пароль'), 'url_name': 'security'},
                                        {'sub_title': _('Выйти'), 'url_name': 'logout'}
                                    )
                                    } 
            #context[ 'account_menu' ] = ACCOUNT_MENU
        else:
            context[ 'account' ] = { 'title': _("Войти"), 'url_name':'auth' }
            #context[ 'register' ] = { 'title': _("Регистрация"), 'url_name':'register' }
            #user_menu.append( { 'title': _('Регистрация'), 'url_name':'register' } )
            #user_menu.append( { 'title': _('Войти'), 'url_name':'login' } )
            context[ 'form_login' ] = AuthLoginForm
        context[ 'menu' ] = user_menu
        return context

