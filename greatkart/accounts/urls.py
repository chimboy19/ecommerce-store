from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'), 
    path('dashboard/',views.dashboard,name='dashboard'), 
    path('',views.dashboard,name='dashboard'), 

    path('activate/<uidb64>/<token>/',views.activate,name='activate'), 
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'), 
    path('resetpassword_vaildate/<uidb64>/<token>/',views.resetpassword_vaildate,name='resetpassword_vaildate'), 
    path('resetpassword/',views.resetpassword,name='resetpassword'), 
    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('order_details/<int:order_id>/',views.order_details,name='order_details')

] 