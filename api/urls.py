
from django.urls import path
from api import views

urlpatterns = [
    path('get_users',views.get_users,name='get_users'),
    path('get_user/<int:pk>',views.get_user,name='get_user'),
    path('get_user_info/<int:pk>',views.get_user_info,name='get_user_info'),

]

