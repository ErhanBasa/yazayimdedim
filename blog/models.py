# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from ckeditor.fields import RichTextField
from django.template.loader import render_to_string
from datetime import datetime
from autoslug import AutoSlugField


class Tag(models.Model):

    name = models.CharField(u"İsim", max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u"Etiket"
        verbose_name_plural = u"Etiketler"


class Category(models.Model):

    name = models.CharField(u"İsim", max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    keywords = models.CharField(u"Anahtar Kelimeler", max_length=255, null=True, blank=True)
    description = RichTextField(u"Açıklama", null=True, blank=True)
    image = models.ImageField(u"Resim", upload_to="category", null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u"Kategori"
        verbose_name_plural = u"Kategoriler"


class Post(models.Model):

    title = models.CharField(u"Başlık", max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    date = models.DateField(u"Tarih")
    keywords = models.CharField(u"Anahtar Kelimeler", max_length=255, null=True, blank=True)
    description = models.TextField(u"Açıklama", null=True, blank=True)
    text = RichTextField(u"Yazı", null=True, blank=True)
    image = models.ImageField(u"Resim", upload_to="post", null=True, blank=True)
    tag = models.ManyToManyField(Tag, null=True, blank=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return "/%s" % self.slug

    class Meta:
        verbose_name = u"Yazı"
        verbose_name_plural = u"Yazılar"


class Contact(models.Model):

    name = models.CharField(u"İsim Soyisim", max_length=255, null=True, blank=True)
    mail = models.EmailField(u"E-Posta Adresiniz", null=True, blank=True)
    subject = models.CharField(u"Konu Neydi?", max_length=255, null=True, blank=True)
    message = models.TextField(u"Mesajınız..")
    date = models.DateTimeField(u"Tarih", default=datetime.now())


class Profile(models.Model):

    profile_picture = models.ImageField(u"Profil Resmi", upload_to="profile", null=True, blank=True)
    about = models.TextField(u"Hakkında", null=True, blank=True)
    user = models.ForeignKey(User)
    facebook_url = models.CharField(u"Facebook Linki", max_length=100, null=True, blank=True)
    twitter_url = models.CharField(u"Twitter Linki", max_length=100, null=True, blank=True)


def contact_handler(sender, instance, signal, *args, **kwargs):
    # Creates user profile
    send_mail(u'Yeni iletişim maili', 
        render_to_string('mails/newmessage.html', {'contact': instance}), 
        settings.EMAIL_HOST_USER, [settings.MY_MAIL])
post_save.connect(contact_handler, sender=Contact)