from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from note.models import Note


def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username=request.COOKIES.get('username')
            c_uid=request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                # 回写session
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)
    return wrap

# Create your views here.
@check_login
def add_note(request):
    if request.method=="GET":
        return render(request,'note/add_note.html')
    elif request.method=="POST":
        uid=request.session['uid']
        title=request.POST['title']
        content=request.POST['content']
        Note.objects.create(title=title, content=content,user_id=uid)
        return HttpResponse("插入成功")
