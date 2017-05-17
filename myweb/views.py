# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404
from myweb.models import h_frontnotes
from myweb.models import hf_artile_sort
from django.forms.models import model_to_dict
from django.conf import settings
import traceback, json, base64, uuid, os

# Create your views here.
try:
    from django.apps import apps as models
except ImportError:  # django < 1.7
    from django.db import models


class MyWeb(object):
    def get_note_menu(self):
        note_sort = []
        new_obj = hf_artile_sort.objects.all()
        for item in new_obj:
            note_sort.append({"text": item.hf_sort_name, "id": item.id})
        return note_sort

    def index(self, request):
        note_sort = self.get_note_menu()
        data = {
            "page": "index",
            "note_sort": note_sort
        }
        return render(request, 'index.html', context=data)

    def life_log(self, request):
        note_sort = self.get_note_menu()
        data = {
            "page": "life_log",
            "note_sort": note_sort
        }
        return render(request, 'life_log.html', context=data)

    def small_note(self, request):
        note_sort = self.get_note_menu()
        data = {
            "page": "small_note",
            "note_sort": note_sort
        }
        return render(request, 'small_note.html', context=data)

    def message_board(self, request):
        note_sort = self.get_note_menu()
        data = {
            "page": "message_board",
            "note_sort": note_sort
        }
        return render(request, 'message_board.html', context=data)

    def h5_game(self, request):
        note_sort = self.get_note_menu()
        data = {
            "page": "h5_game",
            "note_sort": note_sort
        }
        return render(request, 'h5_game.html', context=data)

    def font_note(self, request, *args, **kwargs):
        note_sort = self.get_note_menu()
        sort = kwargs.get("sort")
        page = kwargs.get("page")
        try:
            sort = int(sort)
            page = int(page)
        except:
            raise Exception("传入参数不正确！")
        new_obj = h_frontnotes.objects.filter(hf_artile_cate_id=str(sort)).order_by("-hf_artile_time")[
                  page * 8:(page + 1) * 8]
        frontnotes = []
        title_list = []
        title_number = 1
        for item in new_obj:
            frontnotes_dict = model_to_dict(item)
            frontnotes_dict["artile_date"] = str(item.hf_artile_time)[:19]
            if frontnotes_dict["hf_artile_img"] and frontnotes_dict["hf_artile_content_txt"]:
                title_list.append({"number": title_number, "title": item.hf_artile_title, "id": item.id})
                title_number = title_number + 1
                frontnotes.append(frontnotes_dict)

        data = {
            "page": "font_note",
            "note_sort": note_sort,
            "frontnotes": frontnotes,
            "title_list": title_list[:5]
        }
        return render(request, 'front_note.html', context=data)

    def login(self, request):
        data = {
            "page": "login"
        }
        return render(request, 'login.html', context=data)

    def login_post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/deit_front_note/')
            else:
                return render(request, 'login.html', {"active_msg": u'账户被禁用'})
        else:
            return render(request, 'login.html', {"psd_msg": u'密码错误'})

    def deit_front_note(self, request):
        return render(request, 'ad_front_note.html')

    def save_note(self, request):
        result = {}
        try:
            user = request.user
            note_htm = request.POST.get("note_htm")
            note_txt = request.POST.get("note_txt")
            note_sort = request.POST.get("note_sort")
            title = request.POST.get("title")
            tag = request.POST.get("tag")
            note_path = request.POST.get("image_path")
            path = "/static/images/company-img-1.jpg" if not note_path else note_path

            try:
                new_obj = h_frontnotes.objects.create(hf_artile_title=title, hf_artile_cate_id=note_sort)
                new_obj.hf_artile_content = note_htm
                new_obj.hf_artile_content_txt = note_txt
                new_obj.hf_artile_label = tag if tag else "没有标签"
                new_obj.hf_artile_img = path
                new_obj.save()
                result["sucessful"] = True
            except:
                raise Exception("保存文章出错")


        except Exception, e:
            _trackback = traceback.format_exc()
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result['error_msg'] = err_msg
            result['trackback'] = _trackback
        finally:
            return HttpResponse(json.dumps(result))

    def upload_img(self, request):
        result = None
        try:
            action = request.POST.get("action")
            if action == "front_note":
                file_obj = request.FILES.get("file")
            else:
                file_obj = request.FILES.get("wangEditorH5File")
            if not file_obj:
                raise Exception("没有获取到文件对象！")
            if not request.user.is_authenticated():
                raise Exception("登录用户才可以上传文件！")

            user = request.user
            file_name = str(uuid.uuid1()) + "_" + user.username + '.' + str(file_obj.name.split('.')[-1])
            folder = os.path.join(settings.BASE_DIR, "static", "media", "images")
            if not os.path.exists(folder):
                os.makedirs(folder)
            path = os.path.join(folder, file_name)
            # 保存文件
            fobj = open(path, 'wb')
            for ck in file_obj.chunks():
                fobj.write(ck)
            fobj.close()  # 文件保存完毕
            result = "/".join(["", "static", "media", "images", file_name])
        except Exception, e:
            err_msg = e.message
            if not err_msg and hasattr(e, 'faultCode') and e.faultCode:
                err_msg = e.faultCode
            result = "error|" + err_msg
        finally:
            return HttpResponse(result)

    def view_front_note(self, request, *args, **kwargs):
        note_sort = self.get_note_menu()
        id = kwargs.get("id")
        data = {
            "page": "font_note",
            "note_sort": note_sort,
        }
        return render(request, 'front_notede.html', context=data)
