from django.contrib import admin
from django.urls import path, include
from .forms import *
from .views import *
urlpatterns = [
    path('', ForumNavPage.as_view(), name='forum' ),
    path( '<int:section_id>/', ForumSection.as_view(), name='section'),
    path( '<int:section_id>/<int:post_id>/', ForumPost.as_view(), name='section'),
    path( 'forumservice/', ForumService.as_view(), name='section')
]