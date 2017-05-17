# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib import admin
import myweb.views

myweb_view = myweb.views.MyWeb()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', myweb_view.index),
    url(r'^life_log/$', myweb_view.life_log),
    url(r'^small_note/$', myweb_view.small_note),
    url(r'^message_board/$', myweb_view.message_board),
    url(r'^h5_game/$', myweb_view.h5_game),
    url(r'^font_note/(?P<sort>\w+)/(?P<page>\w+)/$', myweb_view.font_note),
    url(r'^login/$', myweb_view.login),
    url(r'^login_post/$', myweb_view.login_post),
    url(r'^deit_front_note/$', myweb_view.deit_front_note),
    url(r'^save_note/$', myweb_view.save_note),
    url(r'^upload_img/$', myweb_view.upload_img),
    url(r'^view/(?P<id>\w+)/$', myweb_view.view_front_note),

]
