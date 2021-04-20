from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='index'),
    path('products/',views.products,name='products'),
    path('customers/<str:cust_id>',views.customers,name='customers'),
    path('create_order/<str:crt_id>/',views.createOrder,name='create_order'),
    path('update_order/<str:upd_id>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:del_id>/',views.deleteOrder,name='delete_order'),
    path('login/', views.loginPage, name='login'),
    path('user/', views.userPage, name='user-page'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('account/', views.accountSettings, name="account")
]