from django.urls import path
from AuthService.views import *
from django.contrib.auth import views
from .forms import AuthLoginForm

urlpatterns = [
    path( '', AuthLoginView.as_view(), name='auth' ),
    path( 'account', AccountPage.as_view(), name='account' ),
    path( 'security', AuthPasswordChangeView.as_view(), name='security' ),
    #path( '', AuthRgisterView.as_view(), name='account' ),
    # path( 'login/', AuthLoginView.as_view(), name='login', ),
    # path( 'verifi/', AuthEmailVerification.as_view(), name='verifi', ),
    path( 'logout/', AuthLogoutView.as_view(), name='logout' ),

    # path('password_change/', AuthPasswordChangeView.as_view(), name='password_change' ),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done' ),

    # path('password_reset/', AuthPasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    # path('reset/<uidb64>/<token>/', AuthPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('adreses/', AuthService.as_view(), name='adreses'),
    path('authservice/', AuthService.as_view(), name='authservice'),

]