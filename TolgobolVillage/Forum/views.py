from urllib import response
from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView, View
from django.utils.translation import gettext_lazy  as _
from TolgobolVillage.utils import *
from .models import *
from django.http import JsonResponse
from http import HTTPStatus

class ForumNavPage( DataMixin, TemplateView ):
    #form = ProductForm
    template_name = 'Forum/forum_nav.html'
    #model = Product
    title = _("Поселок Толгоболь \ Форум")

    def get_context_data( self, *, object_list=None, **kwargs ):
        print(kwargs)
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

            #result['files']
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
    
    def send_message( self, request):
        print(request.POST)
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
        
        try:
            d = Message.objects.create( **params )
        except:
            print('ХЗ че произошло')
            return JsonResponse( result )
        result['success'] = 'Сообщение сохранено'
        return JsonResponse( result )

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
        print(request.POST)
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

