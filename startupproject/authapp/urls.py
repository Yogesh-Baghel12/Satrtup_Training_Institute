from django.urls import path
from authapp import views
urlpatterns = [
    #function based view
    path('signup/',views.signup,name="signup"),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name='handlelogout'),
    #class based view
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>/',views.SetNewPasswordView.as_view(),name='set-new-password'),

    
]