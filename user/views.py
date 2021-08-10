from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from user.models import User
from user.tool.tools import md5_encryption_tool


def reg_view(request):
    # register
    if request.method == "GET":
        # GET return register.html
        return render(request, 'user/register.html')
    elif request.method == "POST":
        # POST handle submitted data
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        # 1, 两个密码保持一致
        if password_1 != password_2:
            return HttpResponse('两次密码输入不一致')
        # 密码加密
        pwd_md=md5_encryption_tool(password_1)
        # 2,当前用户名是否可用
        old_user = User.objects.filter(username=username)
        if old_user:
            return HttpResponse('用户名已经注册')
        # 3 插入
        try:
            user=User.objects.create(username=username, password=pwd_md)
        except Exception as e:
            # 唯一所应有可能并发写入报错
            print('--create user error %s' % e)
            return HttpResponse('用户名已注册')

        # 免登录一天
        request.session['username']=username
        request.session['uid']=user.id
        # TODO 修改session存储时间为一天
        return HttpResponse('注册成功')
