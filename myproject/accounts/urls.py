from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	# path('logout/', views.logoutUser, name="logout"),
	url(r'^logout/', views.logoutUser, name='logout'),
	path('user/', views.userPage,name='user-page'),
    path('', views.home, name="home"),
    path('products/', views.product, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('account/', views.accountSettings,name="account"),
    

    # path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="updateOrder"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="deleteOrder"),
    # path('create_order/(?P<id>\d+)?$', views.createOrder),
    url(r'^create_order/(?P<id>\d*)$', views.createOrder, name='create_order'),
    path('reset_password',auth_views.PasswordResetView.as_view(),name="reset_password"),
    #password reset django default views 
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    

]