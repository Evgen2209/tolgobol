import time
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView, View
from django.utils.translation import gettext_lazy  as _
from .models import *
from TolgobolVillage.utils import *
import json
from .utils import TmpFileStorage
from datetime import datetime
from django.utils import timezone
from Forum.models import *
import logging

logger = logging.getLogger(__name__)

def str_wrap( *args ):
    st = ''
    for i in args:
        st += str(i)+' '
        return st
    
def log( *args ):
    logger.info( str_wrap( *args ) )
def error( *args ):
    logger.error( str_wrap( *args ) )
def warning( *args ):
    logger.warning( str_wrap( *args ) )
def exception( *args ):
    logger.exception( str_wrap( *args ) )
def debug( *args ):
    logger.debug( str_wrap( *args ) )
    
class HomePage( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'MainService/index.html'
    #model = Product
    title = _("Поселок Толгоболь")

    def get_context_data( self, *, object_list=None, **kwargs ):
        
        c_super = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        c_def[ 'title' ] = self.title
        c_def[ 'news' ] = self.get_news_context()
        c_def.update( c_super )
        return c_def
    
    def get_news_context( self ):
        result = []
        news = Section.objects.filter(is_news=True)
        if news.count():
            for i in news[0].post_set.filter(is_delet=False):
                item = {}
                item['title'] = i.title
                item['preview_text'] = i.text
                item['date'] = i.date
                item['id'] = i.id
                result.append( item )
        return result

class ImportantPage( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'MainService/important.html'
    model = AnyContact
    title = _("Поселок Толгоболь / Важное / Контакты")

    def get_context_data( self, *, object_list=None, **kwargs ):
        c_super = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        c_def['chifs'] = self.get_contact( is_chief=True )
        c_def['anys'] = self.get_contact( is_chief=False )
        c_def[ 'title' ] = self.title
        c_def[ 'votings' ] = self.get_votings_context()
        c_def.update( c_super )
        return c_def
    
    def get_contact( self, is_chief ):
        contacts = AnyContact.objects.filter( is_chief=is_chief )
        res = []
        for i in contacts:
            item = {}
            item['title'] = i.title
            if i.comment != '':
                print('есть')
                item['comment'] = i.comment
            items = []
            for it in i.contactfield_set.all():
                items.append( {'key':it.key, 'value': it.value} )
            item['items'] = items
            res.append( item )
        return res
    def get_votings_context( self ):
        result = []
        votings = Voting.objects.all()
        for voting in votings:
            total_count = voting.votingitemuser_set.count()
            persent = total_count / 100
            item = {}
            if self.request.user.is_authenticated:
                if voting.votingitemuser_set.all().filter(user_id=self.request.user.id).count():
                    item['is_disabled'] = 'disabled'
            if voting.is_finish:
                item['is_disabled'] = 'disabled'
            if voting.finish_data is not None:
                if voting.finish_data < timezone.now().date():
                    item['is_disabled'] = 'disabled'
            item['id'] = voting.id
            item['title'] = voting.title
            item['comment'] = voting.comment
            item['finish_data'] = voting.finish_data if voting.finish_data else 'Без срока'
            item['total_count'] = total_count
            item['voting_items'] = [ dict( [( 'name', i.name ), 
                                            ( 'id', i.id ), 
                                            ( 'voting_persent', int(i.votingitemuser_set.count() / persent) if persent > 0 else 0 ), 
                                            ( 'voting_piople', i.votingitemuser_set.count() ) ] 
                                          ) for i in voting.votingitem_set.all() ]
            result.append( item )
        return result

class CollectionPage( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'MainService/collection.html'
    #model = Product
    title = _("Поселок Толгоболь / Важное / Голосования")

    def get_context_data( self, *, object_list=None, **kwargs ):
        c_super = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        c_def[ 'title' ] = self.title
        c_def[ 'collects' ] = self.get_collect_context()
        c_def[ 'changes' ] = self.get_change_context()
        c_def.update( c_super )
        return c_def
    
    def get_collect_context( self ):
        result = []
        collects = CollectMoney.objects.all()
        self.request.user.is_authenticated
        for collect in collects:
            item = {}
            item['id'] = collect.id
            item['on_months'] = 1 if collect.on_months else 0
            item['title'] = collect.title
            item['comment'] = collect.comment
            item['finish_data'] = collect.finish_data if collect.finish_data is not None else ''
            if self.request.user.is_authenticated:
                item['total_sum'] = collect.get_total_sum()
                item['need_total_summ'] = collect.need_total_summ if collect.need_total_summ else 'Не ограниченно'
                item['available'] = item['total_sum'] - collect.get_sum_charge()
            else:
                item['total_sum'] = 'Авторизуйтесь'
                item['need_total_summ'] = 'Авторизуйтесь'
                item['available'] = 'Авторизуйтесь'

            item['need_summ_on_user'] = collect.need_summ_on_user
            item['files'] = collect.get_files()
            
            if collect.on_months:
                if self.request.user.is_authenticated:
                    item['filter_from_strit'] = collect.filter_from_strit()
            result.append( item )
        return result

    def get_change_context( self ):
        result = []
        charges = FinanceCharge.objects.all()
        for charge in charges:
            item = {}
            item['title'] = charge.title
            item['comment'] = charge.comment
            item['data'] = charge.data if charge.data is not None else ''
            if self.request.user.is_authenticated:
                item['sum'] = charge.charge
            else:
                item['sum'] = 'Авторизуйтесь'
            item['collect_money'] = charge.collect.title
            item['files'] = charge.get_files()
            result.append( item )
        return result
    
class Mainservice( View ):
        
    mainservice_method_alias = {
        'MainService.Voting': 'voting',
        'MainService.FeedbackAdres': 'feedback_adres',
        'MainService.InsertCollectOnMonths': 'insert_collect_on_months',
    }
    
    def dispatch(self, request, *args, **kwargs):
        service_method = request.headers.get( 'X-Requested-MethodName', None ) 
        handler_name = self.mainservice_method_alias.get( service_method, None )
        log( service_method, request.POST )
        if handler_name:
            handler = getattr(
                self, handler_name, self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def voting( self, reqest, *args, **kwargs ):
        respons = {}
        voting_id = reqest.POST['voting_id']
        voting_item_id = reqest.POST['voting_item_id']
        comment = reqest.POST['comment']
        user_id = reqest.user.id
        voting = Voting.objects.get(id=voting_id)
        if not voting.votingitemuser_set.all().filter(user_id=user_id).count():
            VotingItemUser.objects.create( user_id=user_id, voting_id=voting_id, votingitem_id=voting_item_id, comment=comment, data=datetime.now() )
            respons['success'] = 'Ваш голос учтен'
        else:
            respons['error'] = 'Вы уже проголосовали'
        return JsonResponse( respons )
    
    def feedback_adres( self, respons ):
        param = {}
        for i in respons.POST:
            param[i] = respons.POST.get( i )
        FeedbackAdres.objects.create(**param)
        return JsonResponse({})
    
    def insert_collect_on_months( self, respons ):
        errors = []
        collect_id = respons.POST.get( 'collect_id', None)
        adres_id = respons.POST.get( 'adres_id', None)
        insert_list = respons.POST.get( 'insert_list', None)
        
        if insert_list:
            insert_list = json.loads( insert_list )
            
        if not adres_id:
            errors.append(['Не указан адрес', respons.POST ])
        if not adres_id.isdigit():
            errors.append(['адрес не является числом', respons.POST ])
        else:
            adres_id = int(adres_id)

        if not collect_id:
            errors.append(['Не указан collect_id', respons.POST ])
        if not collect_id.isdigit():
            errors.append(['collect_id не является числом', respons.POST ])
        else:
            collect_id = int(collect_id)
        if errors:
            return JsonResponse( {'error': errors}, status=500 )
        try:
            collect = CollectMoney.objects.get(id=int(collect_id))
            adres = Adres.objects.get( id=int(adres_id) )
            for i in insert_list:
                monyh = i['months']
                summ = i['summ']
                year = i['year']
                if not monyh.isdigit():
                    return JsonResponse( {'error': 'monyh не является числом'}, status=500 )
                if not summ.isdigit():
                    return JsonResponse( {'error': 'summ не является числом'}, status=500 )
                if not year.isdigit():
                    return JsonResponse( {'error': 'year не является числом'}, status=500 )
                date_insert = datetime(int(year), int(monyh), 1)
                CollectMoneyMonth.objects.create(collect=collect, adres=adres, strit=adres.strit, month=date_insert, maney=summ)
        except:
            return JsonResponse( {'error': ['Не верные параметры, переданы параметры', respons.POST]}, status=500 )
        return JsonResponse({})
    
    
    
class UploadServise( View ):
        
    mainservice_method_alias = {
        #'UploadingFiles.Upload': 'upload',
        'UploadingFiles.StartUpload': 'start_upload',
        'UploadingFiles.Upload': 'upload',
        'UploadingFiles.FinishUpload': 'finish_upload',
        'UploadingFiles.CancelUpload': 'cancel_upload',
    }
    
    def dispatch(self, request, *args, **kwargs):
        print()
        service_method = request.headers.get( 'X-Requested-MethodName', None ) 
        handler_name = self.mainservice_method_alias.get( service_method, None )
        print( service_method, request.POST )
        if handler_name:
            handler = getattr(
                self, handler_name, self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)    
    
    def start_upload( self, request ):
        if not request.user.is_authenticated:
            return JsonResponse({'error':'Авторизуйтесь'}, status=500)
        error = []
        file_name = request.POST.get( 'file_name', None )
        size = request.POST.get( 'size', None )
        if not file_name or not size:
            error.append( 'Не верные параметры запроса' + str(request.POST) )
            error.append( request.POST )
        if error:
            return JsonResponse({'error':'Не верные параметры запроса' + str(request.POST)}, status=500)
        
        tmp_name = TmpFileStorage().start_upload( file_name, size, request.user )
        if not tmp_name:
            return JsonResponse({'error':'Ошибка при сохранении файла'}, status=500)
        return JsonResponse({'success':tmp_name})
    
    def upload( self, request ):
        strim = request.FILES.get( 'file', None )
        tmp_name= request.POST.get( 'tmp_name', None )
        error = []
        if not strim or not tmp_name:
            error.append( 'Не верные параметры запроса' )
            error.append( request.POST )
            return JsonResponse({'error':error}, status=500)
        try:
            TmpFileStorage().upload( tmp_name, strim.read() )
            return JsonResponse({'success':tmp_name})
        except:
            return JsonResponse({'error':'Ошибка при частичном сохранении файла'}, status=500)
    
    def finish_upload( self, request ):
        tmp_name= request.POST.get( 'tmp_name', None )
        error = []
        if  not tmp_name:
            error.append( 'Не верные параметры запроса' )
            error.append( request.POST )
            return JsonResponse({'error':error}, status=500)
        try:
            id = TmpFileStorage().finish_upload( tmp_name )
            return JsonResponse({'success':id})
        except:
            return JsonResponse({'error':'Ошибка при частичном сохранении файла'}, status=500)
    
    
    def cancel_upload( self, request ):
        tmp_name= request.POST.get( 'tmp_name', None )
        error = []
        if  not tmp_name:
            error.append( 'Не верные параметры запроса' )
            error.append( request.POST )
            return JsonResponse({'error':error}, status=500)
        TmpFileStorage().cancel_upload( tmp_name )
        return JsonResponse({'success':"OK"})