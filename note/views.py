import calendar
import csv
import time

from django.core.paginator import Paginator
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
    page_num = request.GET.get("page",1)
    user_id=request.session['uid']
    noteList = Note.objects.filter(user_id=user_id)
    p = Paginator(noteList,5)
    page_obj=p.get_page(page_num)
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

# 硬删除
@check_login
def notedelete_view(request,id):
    note_info = Note.objects.get(id=int(id))
    if note_info:
        try:
            note_info.delete()
            return HttpResponseRedirect("/note/list")
        except :
            return HttpResponse('删除失败')

@check_login
def produce_csv_view(request):
    page_num = request.GET.get("page", 1)
    user_id = request.session['uid']
    noteList = Note.objects.filter(user_id=user_id)
    p = Paginator(noteList, 5)
    page_obj = p.get_page(page_num)

    ts = calendar.timegm(time.gmtime())
    response=HttpResponse(content_type="text/csv", headers={'Content-Disposition': 'attachment; filename="%s.csv"' % (ts)})
    writer = csv.writer(response)
    writer.writerow(["id","标题", "内容", "创建时间", "修改时间", "作者"])
    for note in page_obj:
        c_time="%s-%s-%s %s:%s:%s" % (note.created_time.year,note.created_time.month,note.created_time.day,note.created_time.hour,note.created_time.minute,note.created_time.second)
        u_time="%s-%s-%s %s:%s:%s" % (note.updated_time.year,note.updated_time.month,note.updated_time.day,note.updated_time.hour,note.updated_time.minute,note.updated_time.second)
        writer.writerow([note.id,note.title,note.content,c_time,u_time,note.user.username])
    return response