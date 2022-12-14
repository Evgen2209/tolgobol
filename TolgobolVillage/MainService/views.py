from django.views.decorators.csrf import ensure_csrf_cookie
import time
from urllib import request
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
from django.urls.base import reverse_lazy
from .logger import *
import pandas as pd
from django.views.static import serve
    
class HomePage( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'MainService/index.html'
    #model = Product
    title = _("Поселок Толгоболь")

    @logger
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
                item['url'] = reverse_lazy( 'post', kwargs={'section_id':str(news[0].id), 'post_id':str(i.id) }  )
                result.append( item )
        return result

class ImportantPage( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'MainService/important.html'
    model = AnyContact
    title = _("Поселок Толгоболь / Важное / Контакты")

    @logger
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
            item = {}
            if voting.is_non_auth:
                if self.request.user.is_authenticated:
                    if voting.votingitemusernonauth_set.all().filter(csrf=str(self.request.user.id)).count():
                        item['is_disabled'] = 'disabled'
                else:
                    csrf = self.request.COOKIES.get( 'csrftoken', None )
                    if voting.votingitemusernonauth_set.all().filter(csrf=csrf).count():
                        item['is_disabled'] = 'disabled'
                if voting.is_finish:
                    item['is_disabled'] = 'disabled'
                if voting.finish_data is not None:
                    if voting.finish_data < timezone.now().date():
                        item['is_disabled'] = 'disabled'
                item['id'] = voting.id
                item['is_non_auth'] = voting.is_non_auth
                item['title'] = voting.title
                item['comment'] = voting.comment
                item['finish_data'] = voting.finish_data if voting.finish_data else 'Без срока'
                total_count = voting.votingitemusernonauth_set.count()
                persent = total_count / 100
                item['voting_items'] = [ dict( [( 'name', i.name ), 
                                                ( 'id', i.id ), 
                                                ( 'voting_persent', int(i.votingitemusernonauth_set.count() / persent) if persent > 0 else 0 ), 
                                                ( 'voting_piople', i.votingitemusernonauth_set.count() ) ] 
                                            ) for i in voting.votingitem_set.all() ]
            else:
                if self.request.user.is_authenticated:
                    if voting.votingitemuser_set.all().filter(user_id=self.request.user.id).count():
                        item['is_disabled'] = 'disabled'
                if voting.is_finish:
                    item['is_disabled'] = 'disabled'
                if voting.finish_data is not None:
                    if voting.finish_data < timezone.now().date():
                        item['is_disabled'] = 'disabled'
                item['id'] = voting.id
                item['is_non_auth'] = voting.is_non_auth
                item['title'] = voting.title
                item['comment'] = voting.comment
                item['finish_data'] = voting.finish_data if voting.finish_data else 'Без срока'
                total_count = voting.votingitemuser_set.count()
                persent = total_count / 100
                item['voting_items'] = [ dict( [( 'name', i.name ), 
                                                ( 'id', i.id ), 
                                                ( 'voting_persent', int(i.votingitemuser_set.count() / persent) if persent > 0 else 0 ), 
                                                ( 'voting_piople', i.votingitemuser_set.count() ) ] 
                                            ) for i in voting.votingitem_set.all() ]
            item['total_count'] = total_count
            result.append( item )
        return result

class CollectionPage( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'MainService/collection.html'
    #model = Product
    title = _("Поселок Толгоболь / Важное / Голосования")

    @logger
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
        'MainService.GetExcelCollect': 'get_excel_collect',
    }
    
    def dispatch(self, request, *args, **kwargs):
        service_method = request.headers.get( 'X-Requested-MethodName', None ) 
        handler_name = self.mainservice_method_alias.get( service_method, None )
        INFO( service_method, request.POST )
        if handler_name:
            handler = getattr(
                self, handler_name, self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
    
    @logger
    def voting( self, reqest, *args, **kwargs ):
        respons = {}
        voting_id = reqest.POST['voting_id']
        voting = Voting.objects.get(id=voting_id)
        if voting.is_non_auth:
            return self.voting_non_auth( reqest, voting )
        
        voting_item_id = reqest.POST['voting_item_id']
        comment = reqest.POST['comment']
        if reqest.user.is_authenticated:
            user_id = reqest.user.id
            if not voting.votingitemuser_set.all().filter(user_id=user_id).count():
                VotingItemUser.objects.create( user_id=user_id, voting_id=voting_id, votingitem_id=voting_item_id, comment=comment, data=timezone.now() )
                respons['success'] = 'Ваш голос учтен'
            else:
                respons['error'] = 'Вы уже проголосовали'
            return JsonResponse( respons )
        else:
            respons['error'] = 'Авторизуйтесь'
            return JsonResponse( respons )
    
    def voting_non_auth( self, reqest, voting ):
        respons = {}
        voting_id = reqest.POST['voting_id']
        voting_item_id = reqest.POST['voting_item_id']
        comment = reqest.POST['comment']
        csrf = reqest.COOKIES.get( 'csrftoken', None )
        if not voting.votingitemusernonauth_set.all().filter(csrf=csrf).count():
            if reqest.user.is_authenticated:
                VotingItemUserNonAuth.objects.create( csrf=str( reqest.user.id ), voting_id=voting_id, votingitem_id=voting_item_id, comment=comment, data=timezone.now() )
            else:
                VotingItemUserNonAuth.objects.create( csrf=csrf, voting_id=voting_id, votingitem_id=voting_item_id, comment=comment, data=timezone.now() )
            respons['success'] = 'Ваш голос учтен'
        else:
            respons['error'] = 'Вы уже проголосовали'
        return JsonResponse( respons )
    
    @logger
    def feedback_adres( self, respons ):
        param = {}
        for i in respons.POST:
            param[i] = respons.POST.get( i )
        FeedbackAdres.objects.create(**param)
        return JsonResponse({})
    
    @logger
    def insert_collect_on_months( self, respons ):
        collect_id = respons.POST.get( 'collect_id', None)
        adres_id = respons.POST.get( 'adres_id', None)
        insert_list = respons.POST.get( 'insert_list', None)
        log = {'collect_id':collect_id,'adres_id': adres_id, 'insert_list':insert_list  }
        INFO( '[insert_collect_on_months] ', log )
        if insert_list:
            insert_list = json.loads( insert_list )
            
        if not adres_id:
            return JsonResponse( {'error': 'Не указан адрес, обратитесь к администратору'}, status=500 )
        if not adres_id.isdigit():
            return JsonResponse( {'error': 'адрес не является числом, обратитесь к администратору'}, status=500 )
        else:
            adres_id = int(adres_id)

        if not collect_id:
            return JsonResponse( {'error': 'Не указан collect_id, обратитесь к администратору'}, status=500 )
        if not collect_id.isdigit():
            return JsonResponse( {'error': 'collect_id не является числом, обратитесь к администратору'}, status=500 )
        else:
            collect_id = int(collect_id)
        try:
            adres = Adres.objects.get( id=int(adres_id) )
            for i in insert_list:
                months = i['months']
                summ = i['summ']
                year = i['year']
                if not months.isdigit():
                    return JsonResponse( {'error': 'months не является числом, обратитесь к администратору'}, status=500 )
                if not summ.isdigit():
                    return JsonResponse( {'error': 'summ не является числом, обратитесь к администратору'}, status=500 )
                if not year.isdigit():
                    return JsonResponse( {'error': 'year не является числом, обратитесь к администратору'}, status=500 )
                date_insert = datetime(int(year), int(months), 1)
                el = CollectMoneyMonth.objects.create(collect_id=collect_id, adres=adres, strit=adres.strit, month=date_insert, maney=summ)
                if not el:
                    return JsonResponse( {'error': 'Данные не внесены, обратитесь к администратору'}, status=500 )
        except Exception as e:
            EXCEPT( e )
            return JsonResponse( {'error': ['Не верные параметры, переданы параметры', respons.POST]}, status=500 )
        return JsonResponse({})
    
    def get_excel_collect( self, reqest ):
        collect_id = reqest.POST.get( 'collect_id', None)
        if not collect_id:
            return JsonResponse( {'error': 'Не указан collect_id'}, status=500 )
        collect = CollectMoney.objects.get( id=int(collect_id) )
        if collect.on_months:
            data = {}
            collect_money = collect.collectmoneymonth_set.all()
            adres_set = collect_money.values('adres')
            adres_set = set( [ i['adres'] for i in adres_set ] )
            moynth_set = collect_money.values('month')
            moynth_set = list( set( [ i['month'] for i in moynth_set ] ) )
            adres_column = {}
            for i in adres_set:
                adr = Adres.objects.get(id=i)
                adres_column[( str(adr) )] = adr
            data['Адрес'] = adres_column.keys()
            moynth_set.sort()
            for month in moynth_set:
                month_column = []
                for ad in adres_column.values():
                    sum = collect_money.filter(month=month, adres_id=ad.id )
                    if sum:
                        month_column.append(sum[0].maney)
                    else:
                        month_column.append(0)
                data[month] = month_column
            df = pd.DataFrame( data )
            file_path = os.path.join( TmpFileStorage.get_tmp_folder(reqest.user.id), f'{collect.title}.xlsx')
            writer = pd.ExcelWriter( file_path ) 
            df.to_excel(writer)
            writer.save()
            path = TmpFileStorage.save_file( file_path )
            return JsonResponse( {'url': reverse_lazy('media', kwargs={ 'path':path })}, status=200 )

    
class UploadServise( View ):
        
    mainservice_method_alias = {
        #'UploadingFiles.Upload': 'upload',
        'UploadingFiles.StartUpload': 'start_upload',
        'UploadingFiles.Upload': 'upload',
        'UploadingFiles.FinishUpload': 'finish_upload',
        'UploadingFiles.CancelUpload': 'cancel_upload',
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
    
    @logger
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
    
    @logger
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
    
    @logger
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
    
    @logger
    def cancel_upload( self, request ):
        tmp_name= request.POST.get( 'tmp_name', None )
        error = []
        if  not tmp_name:
            error.append( 'Не верные параметры запроса' )
            error.append( request.POST )
            return JsonResponse({'error':error}, status=500)
        TmpFileStorage().cancel_upload( tmp_name )
        return JsonResponse({'success':"OK"})