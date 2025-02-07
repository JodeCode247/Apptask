from django.contrib import admin
from .models import MyUsers,AdminApps,UserProfile,UserAppDownload
# Register your models here.
admin.site.register(MyUsers)
admin.site.register(UserProfile)
admin.site.register(AdminApps)
admin.site.register(UserAppDownload)
#admin.site.register(Classrooms)
#admin.site.register(Results)
#admin.site.register(Session)