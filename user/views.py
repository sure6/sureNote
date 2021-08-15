import json

from django.http import HttpResponse, HttpResponseRedirect
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
        return HttpResponseRedirect('/index')


def login_view(request):
    if request.method=="GET":
        # 检查登录状态, 如果有显示'已登录'
        # 检查session
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
        # 没有session, 检查cookies,如果有则回写session
        c_username=request.COOKIES.get('username')
        c_uid=request.COOKIES.get('uid')
        if c_username and c_uid:
            # 回写session
            request.session['username']=c_username
            request.session['uid']=c_uid
            return HttpResponseRedirect('/index')
        # 如果都没有则回到登录页面
        return render(request,'user/login.html')
    elif request.method=="POST":
        uname=request.POST['username']
        pword=request.POST['password']

        # 判断是否有cookie

        if uname=="" or pword=="":
            tips={
                "error":"用户名和密码不能为空"
            }
            return HttpResponse(json.dumps(tips,ensure_ascii=False))

        try:
            old_user = User.objects.get(username=uname)
        except Exception as e:
            print('--user or password error %s' % e)
            tips={
                "error":"用户名和密码不正确"
            }
            return HttpResponse(json.dumps(tips, ensure_ascii=False))

        if  md5_encryption_tool(pword)!=old_user.password:
            tips = {
                "error": "用户名和密码不正确"
            }
            return HttpResponse(json.dumps(tips, ensure_ascii=False))

        # 记录会话状态
        request.session['username']=uname
        request.session['uid']=old_user.id
        redirect={
            "success":"登录成功"
        }
        resp = HttpResponse(json.dumps(redirect, ensure_ascii=False))
        # 判断用户是否'记住用户名'
        if 'check_remember' in request.POST:
            resp.set_cookie('username',uname,expires=3*24*60*60)
            resp.set_cookie('uid',old_user.id,expires=3*24*60*60)

        return resp

def logout_view(request):
    # 删除session
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    # 删除cookies
    resp = HttpResponseRedirect('/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie("username")
    if 'uid' in request.COOKIES:
        resp.delete_cookie("uid")
    return resp



