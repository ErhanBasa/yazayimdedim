# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import Tag, Category, Post, Contact, Profile


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Contact)
admin.site.register(Profile)