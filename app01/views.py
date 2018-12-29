from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def reg(request):
    state=''
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        if User.objects.filter(username=username):
            state='user_exist'
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('/login/')
    content={
        'state':state,
        'user':None,
    }
    return render(request, 'reg.html' ,locals())

def login(request):
    if request.method=='POST':
        name = request.POST.get("username")
        pwd = request.POST.get("pwd")
        user = auth.authenticate(username=name, password=pwd)
        if user is not None:
            auth.login(request,user)
            return redirect('/index/')
    return render(request, 'login.html')

def index(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    return render(request,'index.html')

@login_required()
def change_pwd(request):
    user = request.user
    state=''
    if request.method=='POST':
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        repeat_pwd = request.POST.get('repeat_pwd')
        if user.check_password(old_pwd):
            if not new_pwd:
                state='empty'
            elif new_pwd!=repeat_pwd:
                state='repeat_error'
            else:
                user.set_password(new_pwd)
                user.save()
                return redirect('/login/')
    content={
        'user':user,
        'state':state
    }
    return render(request, 'change_pwd.html', locals())

def logout(request):
    auth.logout(request)
    return redirect('/login/')

# #方法一
# def index(request):
#     '''
#     用户登录后才能访问该页面
#     如果用户没有登录就访问该页面的话直接跳转到登录页面
#     用户在跳转的登录页面完成登陆后，自动访问跳转到之前访问的地址
#     '''
#     if not request.user.is_authenticated():
#         return redirect('%s?next=%s'%(settings.LOGIN_URL, request.path))
#     #若用户没有登录，则会跳转到django默认的登录URL'/accounts/login/'(这个值可以在settings文件中通过LOGIN_URL进行更改)
#     #并传递当前访问url的绝对路径（登录成功后，会重定向到该路径）
#     return render(request, 'index.html')
#
# #方法二
# #Django为我们设计好了一个用于此种情况的装饰器：login_required()
# @login_required
# def index(request):
#     pass










