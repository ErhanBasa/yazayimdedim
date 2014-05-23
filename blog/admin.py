# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import Tag, Category, Post, Contact, Profile
from blog.utils import send_mail_with_template


class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change and request.user != obj.user and obj.is_active:
            send_mail_with_template(u'Yazın onaylandı!', obj.user.email,
                                    'mails/post-accepted.html')
        super(PostAdmin, self).save_model(request, obj, form, change)


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Contact)
admin.site.register(Profile)