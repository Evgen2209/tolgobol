from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from .models import *
from .utils import *
from django.utils.translation import gettext_lazy  as _
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm, UsernameField, SetPasswordForm
import re


class AuthLoginForm( AuthenticationForm ):
    error_messages = {
        'invalid_login': _(
            "Пожалуйста, введите правильные  %(username)s и пароль."
        ),
        'inactive': _("Эта учетная запись неактивна."),
    }

    def __init__( self, *args, **kwargs ):
        super( AuthLoginForm, self ).__init__( *args, **kwargs )
        
    def clean_username( self ):
        user = self.cleaned_data['username']
        try:
            a = User.objects.get( username=user )
        except:
            raise forms.ValidationError( _('Пользователь не существует') )
        if not a.is_active:
            raise forms.ValidationError( _('Пользователь заблокирован') )
        return user

class AuthRegisterUserForm(  UserCreationForm ):

    password1 = forms.CharField( label=_('Пароль *'), widget=forms.PasswordInput, help_text=_('Пароль должен быть не менее 6 символов, состоять из букв и цифр') )
    password2 = forms.CharField( label=_('Повторно пароль *'), widget=forms.PasswordInput)

    def __init__( self, *args, **kwargs ):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ( 'adres', 'first_name', 'last_name', 'patronymic', 'male', 'username', 'birthday', 'email', 'telephon', )
        labels = {
            'first_name': _('Имя *'),
            'last_name': _('Фамилия'),
            'email': _('Email *'),
            'telephon': _('Телефоне'),
            'username': _('Логин *'),
        }
        help_texts = {
            'username': "Введите логин",
        }
        error_messages = {
            'username': {
                'unique': _("Пользователь с таким логином уже существует")
            },
            'email': {
                'unique': _("Пользователь с таким email уже существует")
            },
        }
    
    def clean_username( self ):
        username = self.cleaned_data['username']
        if re.search( '.*\s.*', username ):
            raise forms.ValidationError( _('Не допускаются пробельные символы') )
        if re.search( '.*[А-Яа-я].*', username ):
            raise forms.ValidationError( _('Разрешены только латинские буквы') )
        return username
        
    def clean_password2( self ):
        cd = self.cleaned_data
        pas = cd['password1']
        if pas != cd['password2']:
            raise forms.ValidationError( _("Пароль не совпадает") )
        if len( pas ) < 6:
            raise forms.ValidationError( _('Пароль должен быть не менее 6 символов, состоять из букв и цифр') )
        if not re.search( '\d.*\D|\D.*\d', pas ):
            raise forms.ValidationError( _('Должна быть хотя бы одна цифра и буква') )
        if re.search( '.*\s.*', pas ):
            raise forms.ValidationError( _('Не допускаются пробельные символы') )
        if re.search( '.*[А-Яа-я].*', pas ):
            raise forms.ValidationError( _('Разрешены только латинские буквы') )
        return cd['password2']
    
    # def clean_adres( self ):
    #     print(self.request, 'self.cleaned_data')
    #     user = User.objects.filter( adres_id=self.cleaned_data['adres'] )
    #     if User.objects.filter( adres_id=self.cleaned_data['adres'] ).count():
    #         raise ValidationError( _(f'Пользователь с таким адресом уже существует') )
    #     return self.cleaned_data['adres']

    def clean_telephon( self ):
        if User.objects.filter( telephon=self.cleaned_data['telephon'] ).count():
            raise ValidationError( _(f'Такой телефон уже существует') )
        return validate_telephon( self.cleaned_data['telephon'] )
    
    def clean_email( self ):
        if User.objects.filter( email=self.cleaned_data['email'] ).count():
            raise ValidationError( _(f'Такой Email уже существует') )
        return validate_email( self.cleaned_data['email'] )
    
    def save(self, commit=True):
        # Так как модель User имеет поле ManyToManyField то переопределяю метод save так как в нем идет вызов super().save(commit=False)
        user = super(UserCreationForm, self).save(commit=True)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    def clean(self):
        return super().clean()

class AuthSetPasswordForm( SetPasswordForm ):
    error_messages = {
        'password_mismatch': _('Новые пароли не совпадают'),
    }
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_('Пароль должен быть не менее 6 символов, состоять из букв и цифр'),
    )
    new_password2 = forms.CharField(
        label=_("Повторно новый пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

class AuthPasswordChangeForm( AuthSetPasswordForm ):
    
    error_messages = {
        **AuthSetPasswordForm.error_messages,
        'password_incorrect': _("Ваш старый пароль был введен неправильно. Пожалуйста, введите его еще раз."),
    }
    old_password = forms.CharField(
        label=_("Старый пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
