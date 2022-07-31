
from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from django.views.generic.edit import CreateView, FormView
from .forms import *
from .models import *
from TolgobolVillage.utils import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordContextMixin, PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.urls.base import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import ListView, View, TemplateView
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login
from .utils import *
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin

class AuthLoginView( DataMixin, LoginView ):
    
    form_class = AuthLoginForm
    model = User
    template_name = 'auth.html'
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

    def get_context_data( self, *, object_list=None, **kwargs ):
        result = {}
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context( title=_('Авторизация') )
        result.update( context )
        result.update( c_def )
        strits = Strit.objects.all()
        result['strits'] = strits
        result['register_form'] = AuthRegisterUserForm
        return result

class AuthLogoutView( LogoutView ):
    next_page = reverse_lazy('home')
    
class AuthRgisterView( DataMixin, CreateView ):
    form_class = AuthRegisterUserForm
    template_name = 'auth.html'
    success_url = 'home'

    def get_context_data( self, *, object_list=None, **kwargs ):
        result = {}
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context( title=_('Регистрация') )
        result.update( context )
        result.update( c_def )
        strits = Strit.objects.all()
        result['strits'] = strits
        result['login_form'] = AuthLoginForm
        return result
            
class AuthPasswordChangeView( LoginRequiredMixin, DataMixin, PasswordChangeView ):
    form_class = AuthPasswordChangeForm
    login_url = 'auth'
    redirect_field_name = 'next'

    success_url = reverse_lazy('security')
    template_name = 'security.html'
    title = _('Изминения пароля')

    def get_context_data( self, *, object_list=None, **kwargs ):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context( title=_('Изминения пароля') )
        return { **context, **c_def }
    
class AuthPasswordResetView( DataMixin, PasswordResetView ):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('main')
    template_name = 'registration/password_reset.html'
    title = _('Восстановление пароля')
    token_generator = default_token_generator
    
    def get_context_data( self, *, object_list=None, **kwargs ):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return { **context, **c_def }

class AuthPasswordResetConfirmView( PasswordContextMixin, FormView ):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

class AuthEmailVerification( DataMixin, FormView ):
    form = None
    template_name = 'login/index.html'
    model = None
    title = _("Подтверждение Email")
    
    def get( self, request ):
        token = request.GET.get( 'id', '' )
        user_id = request.GET.get( 'user_id', '' )
        if not token and not user_id:
            return redirect( 'about' )
        try:
            user = User.objects.get( user_id=user_id )
        except:
            return redirect( 'about' )
        if token != user.token:
            return redirect( 'about' )
        user.is_active = True
        user.save()
        return redirect( 'login' )
    
    def post( self, request ):
        return redirect( 'about' )


class AccountPage( LoginRequiredMixin, DataMixin, TemplateView ):
    login_url = 'auth'
    redirect_field_name = 'next'
    #form = ProductForm
    template_name = 'account.html'
    #model = Product
    title = _("Личный кабинет")

    def get_context_data( self, *, object_list=None, **kwargs ):
        c_super = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        c_def[ 'title' ] = self.title
        c_def[ 'invite' ] = self.get_invite()
        c_def.update( c_super )
        return c_def

    def get_invite( self ):
        result = self.request.user.user_id.hex
        result = self.request.build_absolute_uri('/')+'auth/?invite='+self.request.user.user_id.hex+'#id=register'
        return result

class AuthService( View ):
        
    # Регистрация метода, обрабатывается в dispatch
    mainservice_method_alias = {
        'AuthService.ChangeUserData': 'change_user_data',
        'AuthService.Register': 'register',
        'AuthService.GetAdres': 'get_adreses_from_strit',
        'AuthService.GetStrit': 'get_strit',
    }
    
    alias_param = {
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'patronymic': 'Отчество',
        'birthday': 'День рождение',
        'email': 'Email',
        'telephon': 'Телефон',
    }
    
    def dispatch(self, request, *args, **kwargs):
        service_method = request.headers.get( 'X-Requested-MethodName', None ) 
        handler_name = self.mainservice_method_alias.get( service_method, None )
        if handler_name:
            handler = getattr(
                self, handler_name, self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
    def change_user_data( self, request, *args, **kwargs ):
        post = request.POST
        post_param = {}
        for  i in post:
            value = post.get( i, None )
            if value:
                post_param[i] = value
        if not post_param:
            return JsonResponse({})
        user = User.objects.filter( id=request.user.id )
        change_param = {}
        for field, value in post_param.items():
            if user.values()[0][field] != value:
                change_param[field] = post_param[field]

        if 'email' in change_param:
            if User.objects.filter( email=change_param['email'] ).count():
                return JsonResponse({'errors': {'email':'Такой Email уже существует'}})
            try:
                change_param['email'] = validate_telephon( change_param['email'] )
            except Exception as e:
                return JsonResponse({'errors': {'email':'Email '+e.message}})

        if 'telephon' in change_param:
            if User.objects.filter( telephon=change_param['telephon'] ).count():
                return JsonResponse({'errors': {'email':'Такой телефон уже существует'}})
            try:
                change_param['telephon'] = validate_telephon( change_param['telephon'] )
            except Exception as e:
                return JsonResponse({'errors': {'telephon':'Телефон '+e.message}})
            
        user.update(**change_param)
        return JsonResponse( change_param )
    
    def get_adreses_from_strit( self, request ):
        strit_id = request.POST.get('strit_id', None)
        hause_name = request.POST.get('hous', None)
        kv = request.POST.get('kv', None)
        response = {}
        if strit_id is None:
            response['error'] = 'Не верные параметры запроса'
            return JsonResponse(response)
        param = {'strit_id':int(strit_id)}
        if hause_name:
            param['hous'] = hause_name
        if kv:
            param['kv'] = kv
        adreses = Adres.objects.filter(**param)
        bauf = []
        check = []
        for i in adreses:
            if i.hous in check:
                continue
            bauf.append( {'id': i.id, 'hous': i.hous, 'strit_id': i.strit_id, 'kv': i.kv} )
            if not hause_name:
                check.append(i.hous)

        response['adres'] = bauf
        return JsonResponse(response)

    def register( self, request ):
        invite = self.request.POST.get( 'invite', None )
        users = User.objects.filter( adres_id=self.request.POST['adres'] )
        is_invete = False
        if users.count():
            if not invite:
                return JsonResponse( {'errors':{'adres':'Пользователь с таким адресом уже существует, попросите у него инвайт'}} )
            invite = uuid.UUID(invite)
            for user in users:
                if user.user_id == invite:
                    is_invete = True
        else:
            is_invete = True
        if not is_invete:
            return JsonResponse( {'errors':{'adres':'Инвайт код не соответствует адресу'}} )
        servise = AuthRgisterView.as_view()
        respons = self.respons_to_json( servise( request ) )
        return respons

    def respons_to_json( self, respons ):
        from django.template.response import TemplateResponse
        from django.http.response import HttpResponseRedirect
        res = {}
        if isinstance( respons, TemplateResponse ):
            errors = {}
            form = respons.context_data.get( 'form', None )
            if form:
                for field in form:
                    if len( field.errors.data ):
                        errors[field.name] = field.errors.data[0].message
            res['errors'] = errors
        elif isinstance( respons, HttpResponseRedirect):
            res['success'] = respons.headers['Location']
        return JsonResponse( res )

    def validation_from_register( post ):
        res = None
        adres = post.get( 'adres', None )
        if adres is None:
            res = { 'errors': {'adres': 'Не указан адрес'} }
        else:
            try:
                if not len(Adres.objects.filter(id=adres)):
                    res = { 'errors': {'adres': 'Адрес не существует'} }
            except:
                res = { 'errors': {'adres': 'Адрес не существует'} }
        return res
    
    def get_strit( self, respons ):
        result = {}
        strits = []
        for i in Strit.objects.all():
            strits.append( {'id': i.id, 'strit': i.strit_name} )
        result['strits'] = strits
        return JsonResponse(result)