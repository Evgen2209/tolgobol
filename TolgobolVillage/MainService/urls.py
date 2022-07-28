from calendar import month
from django.contrib import admin
from django.urls import path, include
from .forms import *
from .views import *
from django.db.models import Sum
from datetime import date


urlpatterns = [
    path('', HomePage.as_view(), name='home' ),
    path('important/', ImportantPage.as_view(), name='important' ),
    path('collection/', CollectionPage.as_view(), name='collection' ),
    path('mainservise/', Mainservice.as_view(), name='mainservise' ),
    path('upload/', UploadServise.as_view(), name='uploadservise' ),
]

