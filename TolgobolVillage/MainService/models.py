from django.db import models
from django.utils.translation import gettext_lazy as _
from AuthService.models import *
from django.db.models import Sum
from datetime import date
from django.utils import timezone
import os


class AnyContact( models.Model ):
    title = models.CharField( _('Название контакта'), max_length=100, blank=False, unique=False )
    comment = models.CharField( _('Комментарий'), max_length=1000, blank=True, unique=False )
    is_chief = models.BooleanField( _('Является ли старостой'), default=False )

class ContactField( models.Model ):
    key = models.CharField( _('Название'), max_length=100, blank=False, unique=False )
    value = models.CharField( _('Значение'), max_length=1000, blank=False, unique=False )
    contact = models.ForeignKey( AnyContact, on_delete = models.CASCADE )

class Voting( models.Model ):
    title = models.CharField( _('Заголовок'), max_length=100, blank=False, unique=False )
    comment = models.CharField( _('Комментарий'), max_length=10000, blank=True, unique=False )
    finish_data = models.DateField( _('Окончание голосования'), blank=True, null=True )
    is_finish = models.BooleanField( _('Голосование закончилось'), blank=False, default=False )
    
class VotingItem( models.Model ):
    voting = models.ForeignKey(Voting, on_delete = models.CASCADE)
    name = models.CharField( _('Название пункта голосования'), max_length=100, blank=False, unique=False )

class VotingItemUser( models.Model ):
    voting = models.ForeignKey( Voting, on_delete = models.CASCADE )
    votingitem = models.ForeignKey( VotingItem, on_delete = models.CASCADE )
    user = models.ForeignKey( User, on_delete = models.CASCADE )
    comment = models.CharField( _('Комментарий'), max_length=10000, blank=True, unique=False )
    data = models.DateField( _('Дата голосования'), blank=True, null=True )
    
class CollectMoney( models.Model ):
    title = models.CharField( _('Заголовок'), max_length=100, blank=False, unique=False )
    comment = models.CharField( _('Комментарий'), max_length=10000, blank=True, unique=False )
    finish_data = models.DateField( _('Окончание Сбора'), blank=True, null=True )
    on_months = models.BooleanField( _('По месяцам'), blank=False, default=False )
    need_summ_on_user =  models.IntegerField( _('Необходимая сумма на человека'), blank=True, unique=False, default=0 )
    need_total_summ =  models.IntegerField( _('Необходимая сумма на человека'), blank=True, unique=False, default=0 )

    def get_total_sum( self ):
        result = None
        if self.on_months:
            result = self.collectmoneymonth_set.all().filter(collect_id=self.id).aggregate(Sum('maney'))['maney__sum']
        return result if result is not None else 0

    def get_sum_to_month( self, d: date ):
        result = None
        f_date = date( year=d.year, month=d.month, day=1 )
        if self.on_months:
            result = self.collectmoneymonth_set.all().filter( month=f_date ).aggregate( Sum('maney') )['maney__sum']
        return result if result is not None else 0

    def get_sum_to_strit( self, strit_id: int ):
        result = None
        if self.on_months:
            result = self.collectmoneymonth_set.all().filter(collect=self.id, strit_id=int(strit_id)).aggregate(Sum('maney'))['maney__sum']
        return result if result is not None else 0
    
    def get_files( self ):
        result = {}
        filter = self.collectmoneyfile_set.all().filter(collect_id=self.id)
        if not filter:
            result = dict( [ (file.file_name(), file.path.url) for file in filter ] )
        return filter

    def get_sum_charge( self ):
        charge = FinanceCharge.objects.filter(collect_id=self.id)
        if charge.count():
            return charge.aggregate(Sum('charge'))['charge__sum']
        else:
            return 0

    def filter_from_strit( self ):
        result = []
        if self.on_months:
            strits = Strit.objects.all()
            for strit in strits:
                item = {}
                adres_on_strit = strit.adres_set.all()
                count_adres = adres_on_strit.count()
                summ_on_strit = self.collectmoneymonth_set.all().filter(collect=self.id, strit_id=strit.id).aggregate(Sum('maney'))['maney__sum']
                collect_adres = self.collectmoneymonth_set.all().filter(collect=self.id, strit_id=strit.id).values('adres_id')
                collect_adres = len(set( [ i['adres_id'] for i in collect_adres ] ))
                item['id'] = strit.id
                item['strit'] = strit.strit_name
                item['collect_adres'] = collect_adres
                item['count_adres'] = count_adres
                item['summ_on_strit'] = summ_on_strit if summ_on_strit else 0
                buf = {}
                for adres in adres_on_strit:
                    sum = self.collectmoneymonth_set.all().filter(collect=self.id, adres=adres.id).aggregate(Sum('maney'))['maney__sum']
                    buf[adres.get_adres()] = sum if sum else 0
                item['filter_on_hous'] = buf
                result.append( item )
        return result
    
class CollectMoneyAdres( models.Model ):
    # Если сбор не по месяцам а суммой
    collect = models.ForeignKey( CollectMoney, on_delete = models.CASCADE, blank=False )
    adres = models.ForeignKey( Adres, on_delete = models.CASCADE, blank=False )
    summ =  models.IntegerField( _('Сумма сдана'), blank=False, unique=False, default=0 )
    user = models.ForeignKey( User, on_delete = models.CASCADE, blank=True, null=True )
    user_last_name = models.CharField( _('ФИО'), max_length=100, blank=True, unique=False, null=True )
    strit = models.ForeignKey( Strit, on_delete = models.CASCADE, default=None, blank=False )
    
class CollectMoneyMonth( models.Model ):
    # Если сбор по месяцам, например фонд поселка
    collect = models.ForeignKey( CollectMoney, on_delete = models.CASCADE )
    adres = models.ForeignKey( Adres, on_delete = models.CASCADE, blank=False )
    month = models.DateField( _('Месяц'), blank=True, null=True )
    maney = models.IntegerField( _('Сумма за месяц'), blank=False, unique=False, default=0 )
    user = models.ForeignKey( User, on_delete = models.CASCADE, blank=True, null=True )
    user_last_name = models.CharField( _('ФИО'), max_length=100, blank=True, unique=False, null=True )
    strit = models.ForeignKey( Strit, on_delete = models.CASCADE, blank=False )

    def save( self, *args, **kwargs ):
        f_date = date( year=self.month.year, month=self.month.month, day=1 )
        self.month = f_date
        # Проверка поля на уникальность по нескольким полям сразу
        if not CollectMoneyMonth.objects.filter(maney=self.maney, collect_id=self.collect, month=self.month, adres_id=self.adres).count():
            super().save( *args, **kwargs )
        else:
            pass

def upload_to_collect( instance, filename):
    return os.path.join( 'MainService', 'CollectMoney', 'collect_id_'+str( instance.collect.id ), filename )

class CollectMoneyFile( models.Model ):
    collect = models.ForeignKey( CollectMoney, on_delete = models.CASCADE, blank=False )
    path = models.FileField( upload_to=upload_to_collect)
    
    def file_name( self ):
        return os.path.basename( self.path.name )
    
class FinanceCharge( models.Model ):
    collect = models.ForeignKey( CollectMoney, on_delete = models.CASCADE, blank=False )
    title = models.CharField( _('Заголовок'), max_length=100, blank=False, unique=False )
    comment = models.CharField( _('Комментарий'), max_length=10000, blank=True, unique=False )
    data = models.DateField( _('Дата'), blank=True, null=True )
    charge = models.IntegerField( _('Сколько потраченно'), blank=False, unique=False, default=0 )
            
    def get_files( self ):
        result = {}
        filter = self.financechargefile_set.all().filter(сharge=self.id)
        if not filter:
            result = dict( [ (file.file_name(), file.path.url) for file in filter ] )
        return result

def upload_to_collect_change( instance, filename):
    return os.path.join( 'MainService', 'CollectMoney', 'collect_id_'+str( instance.сharge.collect.id ), filename )

class FinanceChargeFile( models.Model ):
    сharge = models.ForeignKey( FinanceCharge, on_delete = models.CASCADE, blank=False )
    path = models.FileField( upload_to=upload_to_collect_change)
    
    def file_name( self ):
        return os.path.basename( self.path.name )
    def is_image( self ):
        img = (
            '.jpg',
            '.png',
        )
        return self.path.name.endswith( img )


class FeedbackAdres( models.Model ):
    adres = models.CharField( _('Адрес'), max_length=100, blank=True, unique=False )
    name = models.CharField( _('Имя'), max_length=100, blank=True, unique=False )
    contact = models.CharField( _('Контакт'), max_length=100, blank=True, unique=False )
    comment = models.CharField( _('Комментарий'), max_length=100, blank=True, unique=False )
    
class File(models.Model):
    existingPath = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()
    
class FileTmp( models.Model ):
    file_name = models.CharField( _('Имя файла'), unique=False, max_length=100,  blank=False)
    tmp_name = models.CharField( _('Временное имя'), unique=True, max_length=100, blank=False )
    tmp_path = models.CharField( _('Временный путь'), unique=True, max_length=100, blank=False )
    size = models.IntegerField( _('Размер файла'), unique=False, blank=False, null=False)
    date_start = models.DateTimeField( _("date start"), default=timezone.now )
    date_finish = models.DateTimeField( _("date finish"), blank=True, null=True )
    user = models.ForeignKey( User, on_delete = models.SET_NULL, blank=True, null=True )
    

    def delete( self, *args, **kwargs ):
        os.remove( self.tmp_path )
        return super().delete()