from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.utils import timezone
from .manager import  CustomUserManager
from django.utils.translation import gettext_lazy as _
from PIL import Image




class MyUsers(AbstractBaseUser,PermissionsMixin):
    class Role(models.TextChoices):  
        ADMIN = 'ADMIN','Admin'
        USER = 'USER','User'
    user_type = models.CharField(max_length=50, choices=Role.choices)   
    username = models.CharField(max_length=255,null=True,unique=True)
    email = models.EmailField(_("email address"), unique=True)
    created_at  = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects =  CustomUserManager()

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.username:
            return self.username
        else:
            return self.email


class AdminApps(models.Model):
    class Category(models.TextChoices):  
        SOCIAL = 'SOCIAL','Social'
        SPORTS = 'SPORTS','Sports'
        ENTERTAINMENT = 'ENTERTAINMENT','Entertainment'
        EDUCATION = 'EDUCATION','Education'
        EXCERCISE = 'EXCERCISE','Exercise'

    name = models.CharField(max_length=50,null=True,unique=True)
    points_reward = models.CharField(max_length=255,null=True)
    app_icon = models.ImageField( null=True) 
    app_store_link = models.URLField()
    category = models.CharField(max_length=50, choices=Category.choices)
    
    

    def __str__(self):
        return self.name

    

class UserProfile(models.Model):
    user = models.OneToOneField(MyUsers, on_delete = models.CASCADE,related_name='auth_users')
    total_points =models.IntegerField( default=0, blank=True)
    number_of_task_completed = models.IntegerField(default=0,blank=True)

    def __str__(self):
        return self.user.username


class UserAppDownload(models.Model):
    user = models.ForeignKey(MyUsers,on_delete=models.CASCADE)
    app =  models.ForeignKey(AdminApps,on_delete=models.CASCADE, related_name='task_apps')
    screenshot = models.ImageField(null=True)
    task_completed =models.BooleanField(default=False)
    is_approved  = models.BooleanField(default=False)
    download_date = models.DateTimeField(auto_now_add=True) 
    pending = models.BooleanField(default=False)
    
    # def save(self, *args, **kwargs):
    #     if self.screenshot:
    #         img = Image.open(self.screenshot)
    #         img.thumbnail((500, 500))
    #         img.save(self.screenshot.path)
    #     super(UserAppDownload, self).save(*args, **kwargs)
