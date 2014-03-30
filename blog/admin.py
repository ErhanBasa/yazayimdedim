# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import Tag, Category, Post, Contact, Profile


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Contact)
admin.site.register(Profile)