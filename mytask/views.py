from urllib import request
from django.shortcuts import render,redirect
from .models import MyUsers,AdminApps,UserProfile,UserAppDownload
from django.contrib.auth import login,logout
from django.http import HttpResponse,JsonResponse
from functools import wraps



def check_if_user_is_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user == "ADMIN":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('INVALID URL')
    return _wrapped_view



def indexpage(request):
    
    return render(request,'mytask/index.html')


def homepage(request):
    status=''
    #getting the apps apps that it task has been completed by the user, which is still on pending
    approved_apps = UserAppDownload.objects.filter(user=request.user,task_completed=True).values_list('app', flat=True)
       
    query = request.GET.get('query')
    if query:
        apps = AdminApps.objects.exclude(id__in=approved_apps).order_by('name').filter(category__icontains=query)
        
    
    else:
        #this to make sure that the apps displyed are apps whose task has not been completed by the user
        apps = AdminApps.objects.exclude(id__in=approved_apps).order_by('name')
    
     #this part counts the number of pending task
    pending_num = AdminApps.objects.filter(id__in=UserAppDownload.objects.filter(user=request.user,task_completed=True,pending=True).values_list('app', flat=True)).count
    user = UserProfile.objects.get(user=request.user)

    context = {'user':user,'apps':apps,'status':status,'pending_num':pending_num,'home':10,'query':query} 
    return render(request,'mytask/homepage.html',context)



def pendingTask(request):
    status='pending'
    user = UserProfile.objects.get(user=request.user)
   
    approved_apps = UserAppDownload.objects.filter(user=request.user,task_completed=True,pending=True).values_list('app', flat=True)
    print(approved_apps)
  
   
    apps = AdminApps.objects.filter(id__in=approved_apps).order_by('name')
    pending_num =apps.count
    context = {'user':user,'apps':apps,'status':status,'pending_num':pending_num} 
    return render(request,'mytask/homepage.html',context)


@check_if_user_is_admin
def adminPage(request):
    user = request.user
    #gets the pending tasks , to be displays on the admin dashboard
    task_awaiting_approval = UserAppDownload.objects.filter(task_completed=True,is_approved=False)
    
    if request.method == 'POST':
        task_id = int(request.POST.get('task_id'))
        #check to see if the admin declined the task by user
        action = request.POST.get('action')
        if action == 'approve':
            task = task_awaiting_approval.get(id=task_id)
            print(task.app,'yeah')
            task.pending=False
            task.is_approved=True
            task.save()

        if action == 'decline':
            task = task_awaiting_approval.get(id=task_id)
            task.delete()
            return redirect('adminPage')
        person = UserProfile.objects.get(user=task.user)
        app_reward = int(task.app.points_reward)
        total_points=person.total_points+app_reward
        print(total_points)
        person.total_points=total_points
        person.number_of_task_completed +=1
        person.save()
            
    
    context = {'user':user,'task_awaiting_approval':task_awaiting_approval}
    return render(request,'mytask/admin.html',context)

@check_if_user_is_admin
def app_create(request):
    if request.method=='POST':
        name = request.POST.get('app_name').upper()
        app_store_link = request.POST.get('app_store_link')
        points_reward = request.POST.get('points_reward')
        category = request.POST.get('category').upper()
        app_icon = request.FILES.get('app_icon')

        if AdminApps.objects.filter(name=name).exists():
            return HttpResponse('App already exist')

        if category and name:
            try:
                AdminApps.objects.create(name=name,app_store_link=app_store_link,app_icon=app_icon,
                                     points_reward=points_reward,category=category)
                return redirect('app_create')
            except:
               return HttpResponse('app not added to database')
            
    categories=AdminApps.Category.choices
    
    context = {'categories':categories}
    return render(request,'mytask/app-create.html',context)

@check_if_user_is_admin
def submit_task(request,app_id):
    app=AdminApps.objects.get(id=app_id)
    user = UserProfile.objects.get(user=request.user)
    person = MyUsers.objects.get(email=request.user.email)
    if request.method == 'POST':
        print(request.FILES)
        screenshot = request.FILES.get('screenshot')
        if not screenshot:
            print('no image was uploaded')
            return redirect('homepage')
        myapp =UserAppDownload.objects.filter(user=person,app=app)
        if not myapp.exists():

            try:
                x=UserAppDownload.objects.create(user=person,app=app,screenshot=screenshot)
                x.task_completed=True
                x.pending=True
                x.save()
            except:
                return HttpResponse('error occurred')
        
            return HttpResponse('success')
        else:
            myapp.screenshot=screenshot
            data = {'message':'task completed'}
            return JsonResponse(data['message'], safe=False)
    context = {'app':app,'user':user}
    return render(request,'mytask/drop.html',context)

 
def view_all_app(request):
    context = {}
    return render(request,'mytask/all_app.html')

def view_all_user(request):
    users = MyUsers.objects.only('email').order_by('id')

    context = {'users':users}
    return render(request,'mytask/all_users.html',context)



def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username').title()
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_admin = request.POST.get('is_admin')
        print(is_admin)
        
        if is_admin:
            #return HttpResponse('admin')
            user=MyUsers.objects.create_user(username=username,email=email,password=password,user_type=MyUsers.Role.ADMIN,is_staff=True,is_active=True,is_superuser= True)
        else:
            #return HttpResponse('user')
            user= MyUsers.objects.create_user(username=username,email=email,password=password,user_type=MyUsers.Role.USER,is_staff=True,is_active=True)
            if user:
                UserProfile.objects.create(user=user)

        if user:
            return redirect('login')
        

    return render(request,'mytask/registration.html')

@check_if_user_is_admin
def delete_user(request,id):
    if request.method=='POST':
        user=MyUsers.objects.get(id=id)
        user.delete()
        return redirect('view_all_user')

    return render(request,'mytask/delete.html')





def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            try:
                user = MyUsers.objects.get(email = email)
                if user.check_password(password):

                    if user is not None:
                        print(user.email, 'password test passed')
                        login(request,user)
                        if user.user_type == "USER":
                            print('yes normal user')
                            return redirect('homepage')

                        elif user.user_type == "ADMIN":
                            print('yes ADMIN')
                            #return redirect('home')
                            return redirect('adminPage')
                        
                        else:
                            return HttpResponse('user not logged in , due to authentication failure')
                else:
                    return HttpResponse('email or password incorrect')
            except:
                return HttpResponse('user does not exist')
              
    return render(request,'mytask/login.html')


def logout_user(request):
    logout(request)
    #messages.success(request,'you are logged out')
    return redirect('home')