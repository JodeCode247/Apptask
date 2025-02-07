from django.urls import path
from mytask import views


urlpatterns = [
    path('',views.indexpage, name='home'),
    path('profile/',views.homepage, name='homepage'),
    path('submit_task/<int:app_id>',views.submit_task, name='submit_task'),
    path('new_tasks/',views.view_all_app, name='view_all_app'),
    path('pending_task/',views.pendingTask, name='pending_task'),
    


    path('admin_profile/',views.adminPage, name='adminPage'),
    path('add_app/',views.app_create, name='app_create'),
    path('User_manager/',views.view_all_user, name='view_all_user'),
    path('view_all_app/',views.view_all_app, name='view_all_app'),
    path('delete_user/<int:id>',views.delete_user, name='delete_user'),


    path('register/',views.register_user, name='register'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
]