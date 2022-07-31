from urllib import response
from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView, View
from django.utils.translation import gettext_lazy  as _
from TolgobolVillage.utils import *
from .models import *
from django.http import JsonResponse
from http import HTTPStatus
from TolgobolVillage import settings
import logging
import shutil
from django.urls.base import reverse_lazy
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
    
class ForumNavPage( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'Forum/forum_nav.html'
    #model = Product
    title = _("Поселок Толгоболь \ Форум")

    def get_context_data( self, *, object_list=None, **kwargs ):
        c_super = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        c_def[ 'title' ] = self.title
        c_def[ 'nav' ] = self.get_forum_nav_context()
        c_def.update( c_super )
        return c_def

    def get_forum_nav_context( self ):
        result = []
        sections = Section.objects.all()
        for section in sections:
            item = {}
            item['name'] = section.name
            item['id'] = section.id
            posts = section.post_set.all().filter( is_delet=False )
            item['posts'] = posts.count()
            item['messages'] = sum( [ i.message_set.all().filter( is_delet=False ).count() for i in posts  ] )
            sms = section.get_last_message_on_post()
            if sms:
                item['last_message'] = {'post_title': sms.post.title, 'post_id': sms.post.id, 'author': sms.author, 'date': sms.update_date}
            result.append( item )
        return result
    
class ForumSection( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'Forum/forum_section.html'
    #model = Product
    title = _("Поселок Толгоболь \ Форум")

    def get_context_data( self, *, object_list=None, **kwargs ):
        section_id = kwargs['section_id']
        c_super = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        c_def[ 'title' ] = self.title
        c_def[ 'posts' ] = self.get_posts_context( section_id )
        c_def[ 'section_id' ] = section_id
        c_def[ 'is_news' ] = Section.objects.get(id=section_id).is_news
        c_def.update( c_super )
        return c_def
    
    def get_posts_context( self, section_id ):
        result = []
        posts = Post.objects.filter(section_id=section_id)
        for post in posts:
            item = {}
            item['id'] = post.id
            item['title'] = post.title
            item['text'] = post.text
            item['author'] = post.author 
            item['date'] = post.update_date
            item['message_count'] = post.message_set.all().count()
            sms = post.get_last_message()
            if sms:
                item['last_message'] = {'author': sms.author, 'date': sms.update_date}
            result.append( item )
        return result

class ForumPost( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'Forum/forum_post.html'
    #model = Product
    title = _("Поселок Толгоболь \ Форум")

    def get_context_data( self, *, object_list=None, **kwargs ):
        post_id = kwargs['post_id']
        c_super = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        c_def[ 'title' ] = self.title
        c_def[ 'post' ] = self.get_post_context( post_id )
        c_def[ 'post_id' ] = post_id
        c_def.update( c_super )
        return c_def
    
    def get_post_context( self, post_id ):
        result = {}
        try:
            post = Post.objects.get(id=post_id)
            result['title'] = post.title
            result['text'] = post.text
            result['author'] = post.author
            result['date'] = post.date
            if self.request.user.is_authenticated:
                if self.request.user.id == post.author.id:
                    result['self'] = True

            post_files = []
            for f in post.postfile_set.all():
                post_files.append( {'name': f.file_name(), 'url': f.path.url, 'is_img': f.is_image()} )
            result['files'] = post_files
        except:
            return result
        messages = []
        for sms in post.get_messages():
            item = {}
            item['id'] = sms.id
            item['text'] = sms.text
            item['author'] = sms.author 
            item['author_id'] = sms.author_id 
            item['related_message'] = sms.get_related_message()
            files = []
            for f in sms.messagefile_set.all():
                files.append( {'name': f.file_name(), 'url': f.path.url, 'is_img': f.is_image()} )
            item['files'] = files
            if sms.update_date == sms.date:
                item['date'] = sms.date
            else:
                item['update_date'] = sms.update_date
            if self.request.user.is_authenticated:
                if self.request.user.id == sms.author.id:
                    item['self'] = True
            messages.append( item )
        result['messages'] = messages
        return result


class ForumService( View ):
        
    mainservice_method_alias = {
        'ForumService.SendMessage': 'send_message',
        'ForumService.UpdateMessage': 'update_message',
        'ForumService.DeletMessage': 'delete_message',
        'ForumService.PostCreate': 'post_create',
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
    
    def send_message( self, request):
        if not request.user.is_authenticated:
            return JsonResponse( {"error": "Необходима авторизация"}, status=500 )
        result = {}
        error = []
        params = {}
        
        
        related_message = request.POST.get('related_message', None)
        post = request.POST.get('post', None)
        if not post:
            error.append( 'Не указан id_post' )
        params['post'] = post
        text = request.POST.get('text', None)
        if not text:
            error.append( 'Не указан text' )
        if related_message:
            params['related_message'] = int( related_message )
        if error:
            return JsonResponse( {"error": error}, status=500 )
        params['post'] = Post.objects.get( id=int( post ) )
        params['text'] = text
        params['author'] = request.user
        date = timezone.now()
        params['date'] = date
        params['update_date'] = date
        
        files = request.POST.get('files', None)
        try:
            m = Message.objects.create( **params )
            if files:
                
                files = files.split(',')
                for i in files:
                    f = FileTmp.objects.get( id=int(i) )
                    MessageFile.objects.create( message=m, path=self.copy_file(f, m.id) )
        except Exception as e:
            exception(e)
            return JsonResponse( {"error": e}, status=500 )
        result['success'] = 'Сообщение сохранено'
        return JsonResponse( result )

    def copy_file( self, tmp_file, m_id ):
        tmp_path = tmp_file.tmp_path
        name = tmp_file.file_name
        nev_path_folder = os.path.join( settings.MEDIA_ROOT, 'Forum_files', str(m_id) )
        if not os.path.exists( nev_path_folder ):
            os.makedirs(nev_path_folder)
        nev_path = os.path.join( nev_path_folder, name )
        shutil.copyfile( tmp_path, nev_path )
        tmp_file.delete()
        return os.path.relpath( nev_path, settings.MEDIA_ROOT )
            
    def update_message( self, request):
        if not request.user.is_authenticated:
            return JsonResponse( {"error": "Необходима авторизация"}, status=500 )
        sms_id = request.POST.get( 'post', None )
        author_id = request.POST.get( 'author', None )
        text = request.POST.get( 'text', None )
        error = []
        if not sms_id:
            error.append( 'Не указан post' )
        if not author_id:
            error.append( 'Не указан author' )
        if not text:
            error.append( 'Не указан text' )
        if error:
            return JsonResponse( {"error": error}, status=500 )
        sms = Message.objects.get(id=int(sms_id) )
        upade_date = timezone.now()
        HistoryMessage.objects.create( message=sms, text=sms.text, date=upade_date )
        sms.text = text
        sms.upade_date = upade_date
        sms.save()
        result = {}
        result['success'] = 'Сообщение изменено'
        return JsonResponse( result )
    
    def delete_message( self, request ):
        if not request.user.is_authenticated:
            return JsonResponse( {"error": "Необходима авторизация"}, status=500 )
        sms_id = request.POST.get( 'post_id', None )
        author_id = request.POST.get( 'author', None )
        error = []
        if not sms_id:
            error.append( 'Не указан post' )
        if not author_id:
            error.append( 'Не указан author' )
        if error:
            return JsonResponse( {"error": error}, status=500 )
        sms = Message.objects.get( id=int(sms_id) )
        if sms.author_id != int(author_id):
            return JsonResponse( {"error": "Не верно указан author"}, status=500 )
        sms.update_date = timezone.now()
        sms.is_delet = True
        sms.save()
        result = {}
        result['success'] = 'Сообщение удалено'
        return JsonResponse( result )

    def post_create( self, request ):
        if not request.user.is_authenticated:
            return JsonResponse( {"error": "Необходима авторизация"}, status=500 )
        result = {}
        print( request.POST )
        section_id = request.POST.get( 'section_id', None )
        title = request.POST.get( 'title', None )
        text = request.POST.get( 'text', None )
        params = {}
        error = []
        if not section_id:
            error.append( 'Не указан section_id' )
        params['section_id'] = section_id
        if not title:
            error.append( 'Не указан title' )
        params['title'] = title
        if not text:
            error.append( 'Не указан text' )
        params['text'] = text
        
        params['author_id'] = request.user.id
        date = timezone.now()
        params['date'] = date
        params['update_date'] = date
        files = request.POST.get('files', None)
        print(params)
        m = Post.objects.create( **params )
        if files:
            
            files = files.split(',')
            for i in files:
                f = FileTmp.objects.get( id=int(i) )
                PostFile.objects.create( post=m, path=self.copy_file(f, 'post_'+str(m.id) ) )
        result['url'] = reverse_lazy( 'post', kwargs={'section_id':str(section_id), 'post_id':str(m.id) }  )
        print(result)
        return JsonResponse( result )

class PostCreateForm( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'Forum/post_create.html'
    #model = Product
    title = _("Поселок Толгоболь \ Форум")

    def get_context_data( self, *, object_list=None, **kwargs ):
        print(kwargs)
        c_super = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        c_def[ 'title' ] = self.title
        c_def[ 'section_id' ] = kwargs['section_id']
        c_def.update( c_super )
        return c_def
    
    
    