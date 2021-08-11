from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from note.models import Note


# 定义session和cookies校验装饰器
def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
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
def addnote_view(request):
    if request.method == "GET":
        flag="add"
        return render(request, 'note/add_note.html',locals())
    elif request.method == "POST":
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponseRedirect("list")


@check_login
def list_view(request):
    noteList = Note.objects.all()
    return render(request, 'note/list_note.html', locals())


@check_login
def notedetail_view(request):
    if request.method=="GET":
        flag="detail"
        note_id = request.GET.get('id')
        note_info=Note.objects.get(id=note_id)
        return  render(request, 'note/add_note.html', locals())

@check_login
def noteedit_view(request):
    if request.method == "GET":
        flag="edit"
        note_id = request.GET.get('id')
        note_info = Note.objects.get(id=note_id)
        return render(request, 'note/add_note.html',locals())
    elif request.method == "POST":
        content = request.POST['content']
        note_id = request.POST['id']
        note_info = Note.objects.get(id=note_id)
        note_info.content=content
        note_info.save()
        return HttpResponseRedirect("list")
