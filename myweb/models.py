# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models


# Create your models here.
@python_2_unicode_compatible
class h_visitors(models.Model):
    hv_name = models.CharField(u'昵称', max_length=20, null=True)
    hv_email = models.CharField(u'邮箱', max_length=20, null=True)
    hv_web = models.URLField(u'网站')

    def __str__(self):
        return self.hv_name

    class Meta:
        verbose_name = u'游客用户表'


@python_2_unicode_compatible
class h_fwebs(models.Model):
    hfw_name = models.CharField(u'名称', max_length=20, null=True)
    hfw_web = models.URLField(u'网站')

    def __str__(self):
        return self.hfw_name

    class Meta:
        verbose_name = u'友链表'


@python_2_unicode_compatible
class h_frontnotes(models.Model):
    hf_artile_title = models.CharField(u'题目', max_length=100)
    hf_artile_content = models.TextField(u'内容', null=True)
    hf_artile_content_txt = models.TextField(u'内容', null=True)
    hf_artile_cate = models.ForeignKey('myweb.hf_artile_sort', max_length=20)
    hf_artile_time = models.DateTimeField(u'发布日期', auto_now=True)
    hf_artile_label = models.CharField(u'文章标签', max_length=20, null=True)
    hf_artile_img = models.CharField(u'文章图片', max_length=512, null=True)
    write_date = models.DateTimeField(u'更新时间', auto_now=True,null=True)

    def __str__(self):
        return self.hf_artile_title

    class Meta:
        verbose_name = u'前端笔记文章表'


@python_2_unicode_compatible
class hf_artile_sort(models.Model):
    hf_sort_name = models.CharField(u'分类名称', max_length=100)
    hf_sort_describe = models.TextField(u'分类描述', null=True)

    def __str__(self):
        return self.hf_artile_sort

    class Meta:
        verbose_name = u'前端笔记分类表'


@python_2_unicode_compatible
class h_fcomments(models.Model):
    hf_article = models.ForeignKey('myweb.h_frontnotes', verbose_name=u'文章')
    hfc_uid = models.ForeignKey('myweb.h_visitors', verbose_name=u'评论人')
    hfc_puid = models.ForeignKey('auth.user', verbose_name=u'被评论人')
    hfc_content = models.CharField(u'评论内容', max_length=200)
    hfc_time = models.DateField(u'评论日期', auto_created=True, auto_now=True)
    hfc_soft = models.IntegerField(u'评论级别')

    def __str__(self):
        return self.hfc_content

    class Meta:
        verbose_name = u'前端文章评论表'


@python_2_unicode_compatible
class h_lifelogs(models.Model):
    hf_artile_title = models.CharField(u'题目', max_length=100)
    hf_artile_content = models.TextField(u'内容', null=True)
    hf_artile_cate = models.CharField(u'类别', max_length=20)
    hf_artile_time = models.DateField(u'发布日期', auto_now=True, auto_created=True)

    def __str__(self):
        return self.hf_artile_title

    class Meta:
        verbose_name = u'生活日志表'


@python_2_unicode_compatible
class hl_comments(models.Model):
    hl_article = models.ForeignKey('myweb.h_frontnotes', verbose_name=u'文章')
    hlc_uid = models.ForeignKey('myweb.h_visitors', verbose_name=u'评论人')
    hlc_puid = models.ForeignKey('auth.user', verbose_name=u'被评论人')
    hlc_content = models.CharField(u'评论内容', max_length=200)
    hlc_time = models.DateField(u'评论日期', auto_created=True, auto_now=True)
    hlc_soft = models.IntegerField(u'评论级别')

    def __str__(self):
        return self.hlc_content

    class Meta:
        verbose_name = u'生活日志评论表'


@python_2_unicode_compatible
class h_smallnotes(models.Model):
    hu = models.ForeignKey('auth.User', verbose_name=u'发表人')
    hsn_title = models.CharField(u'内容', max_length=200)
    hsn_cate = models.CharField(u'类别', max_length=20)
    hsn_time = models.DateField(u'日期', auto_created=True, auto_now=True)

    def __str__(self):
        return self.hsn_title

    class Meta:
        verbose_name = u'闲言碎语'


@python_2_unicode_compatible
class h_messages(models.Model):
    hv = models.ForeignKey('myweb.h_visitors', verbose_name=u'留言人')
    hmb_title = models.CharField(u'内容', max_length=200)
    hmb_soft = models.IntegerField(u'级别')
    hmb_time = models.DateField(u'日期', auto_created=True, auto_now=True)

    def __str__(self):
        return self.hmb_title

    class Meta:
        verbose_name = u'留言板'


@python_2_unicode_compatible
class h_games(models.Model):
    hg_title = models.CharField(u'游戏名称', max_length=50)
    hg_info = models.CharField(u'简介', max_length=200)
    hg_time = models.DateField(u'日期', auto_created=True, auto_now=True)

    def __str__(self):
        return self.hg_title

    class Meta:
        verbose_name = u'H5小游戏'
