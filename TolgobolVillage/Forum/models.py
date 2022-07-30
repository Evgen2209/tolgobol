from django.db import models
import os
from django.utils.translation import gettext_lazy as _
from AuthService.models import *
from django.utils import timezone

class News( models.Model ):
    title = models.CharField( _('Заголовок'), max_length=100, blank=False, unique=False )
    text = models.CharField( _('Текст Новости'), max_length=90000, blank=True, unique=False )
    preview_text = models.CharField( _('Превью Текст'), max_length=10000, blank=True, unique=False )
    date = models.DateField( _('Дата'), blank=True, null=True )
    logo = models.FileField( upload_to='MainService/News', null=True)
    publish = models.BooleanField( _('Публиковать на главную'), blank=False, default=True )
    user = models.ForeignKey( User, on_delete = models.SET_NULL, null=True, blank=True )

def upload_to_news( instance, filename):
    return os.path.join( 'MainService', 'News', 'news_id_' + str( instance.news.id ), filename )

class NewsFile( models.Model ):
    news = models.ForeignKey( News, on_delete = models.CASCADE, blank=False )
    path = models.FileField( upload_to=upload_to_news)
    
    def file_name( self ):
        return os.path.basename( self.path.name )

class Section( models.Model ):
    name = models.CharField( _('Название раздела'), max_length=100, blank=False, unique=False )
    
    def get_last_message_on_post( self ):
        result = None
        posts = self.post_set.all().filter( is_delet=False ).order_by('message__date')
        if posts.count():
            result = posts.last().get_last_message()
        return result
    
class Post( models.Model ):
    section = models.ForeignKey( Section, on_delete = models.SET_NULL, null=True )
    title = models.CharField( _('Заголовок'), max_length=100, blank=False, unique=False )
    text = models.CharField( _('Текст Новости'), max_length=90000, blank=True, unique=False )
    author = models.ForeignKey( User, on_delete = models.SET_NULL, null=True )
    date = models.DateTimeField( _('Дата создания'), default=timezone.now )
    update_date = models.DateTimeField( _('Дата обновления'), default=timezone.now )
    is_delet =  models.BooleanField( _('Удалена ли запись'), blank=False, default=False )
    is_news =  models.BooleanField( _('Является ли новостью'), blank=False, default=False )
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['date']
        
    def __str__( self ):
        return str( self.title )
    
    def get_last_message( self ):
        result = None
        sms = self.message_set.all().filter( is_delet=False ).order_by('date')
        if sms.count():
            result = sms.last()
        return result
    
    def get_messages( self ):
        buf = self.message_set.filter( is_delet=False )
        buf1 = buf.order_by('date')
        return buf1

def upload_to_post( instance, filename):
    return os.path.join( 'Forum', 'Post', 'post_id_' + str( instance.post.id ), filename )

class PostFile( models.Model ):
    post = models.ForeignKey( Post, on_delete = models.CASCADE, blank=False )
    path = models.FileField( upload_to=upload_to_post )
    
    def file_name( self ):
        return os.path.basename( self.path.name )

class Message( models.Model ):
    post = models.ForeignKey( Post, on_delete = models.CASCADE, blank=False )
    author = models.ForeignKey( User, on_delete = models.SET_NULL, null=True )
    text = models.CharField( _('Текст сообщения'), max_length=90000, blank=True, unique=False )
    date = models.DateTimeField( _('Дата создания'), default=timezone.now )
    update_date = models.DateTimeField( _('Дата обновления'), default=timezone.now )
    is_delet =  models.BooleanField( _('Удалена ли запись'), blank=False, default=False )
    related_message = models.IntegerField( _('Id связанного сообщения'), blank=True, null=True, default=None )
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['update_date']

    def get_related_message( self ):
        if self.related_message:
            sms = Message.objects.get( id=self.related_message )
            return {'post': sms.post, 'author': sms.author,'text': sms.text,'date': sms.update_date, 'id': sms.id}
        return None

class HistoryMessage( models.Model ):
    message = models.ForeignKey( Message, on_delete = models.CASCADE, blank=False )
    text = models.CharField( _('Текст сообщения'), max_length=90000, blank=True, unique=False )
    date = models.DateTimeField( _('Дата изминения'), default=timezone.now )



def upload_to_message( instance, filename):
    return os.path.join( 'Forum', 'Post', 'post_id_' + str( instance.message.post.id ), str( instance.message.author.first_name ), filename )

class MessageFile( models.Model ):
    message = models.ForeignKey( Message, on_delete = models.CASCADE, blank=False )
    path = models.FileField( upload_to=upload_to_message )
    
    def file_name( self ):
        return os.path.basename( self.path.name )

    def is_image( self ):
        img = (
            '.jpg',
            '.png',
        )
        return self.path.name.endswith( img )
