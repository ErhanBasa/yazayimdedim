# -*- coding: utf-8 -*-

from blog.models import Tag, Category, Post, Profile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.syndication.views import Feed
from blog.forms import ContactForm, RegisterationForm, LoginForm as AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as login_func, authenticate, logout as logout_func
from django.contrib.auth.decorators import login_required


def articles(request, template='index.html'):
    tags = Tag.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    posts = Post.objects.all().order_by('-date')

    ctx = {
        'tags': tags,
        'categories': categories,
        'posts': posts,
    }

    return render(request, template, ctx)


def article(request, slug, template='post.html'):
    categories = Category.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    post = get_object_or_404(Post, slug=slug)
    posts = Post.objects.all().exclude(pk=post.pk).order_by('?')[:3]
    category = post.category.all()
    tag = post.tag.all()

    ctx = {
        'categories': categories,
        'category': category,
        'posts': posts,
        'post': post,
        'tags': tags,
        'tag': tag,
    }

    return render(request, template, ctx)


def sitemap(request, template="sitemap.html"):
    posts = Post.objects.all().order_by('-date')

    ctx = {
        'posts': posts,
    }

    return render(request, template, ctx)


class LatestArticlesFeed(Feed):
    title = u"Bunu da yazayım dedim"
    link = ""
    description = u"Yazayimdedim.com'un son yazılarını buradan takip edebilirsiniz."

    def items(self):
        return Post.objects.order_by('-date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()


def contact(request, template="contact.html"):
    if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.SUCCESS, u'Tamamdır')
                    return redirect('contact')
    else:
            form = ContactForm()
    ctx = {
        'form': form,
    }
    return render(request, template, ctx)


def profile(request, slug, template="profile.html"):
    profile = get_object_or_404(Profile, user__username=slug)
    posts = Post.objects.filter(user=profile.user)

    ctx = {
        'profile': profile,
        'posts': posts,
    }

    return render(request, template, ctx)


def login(request, template="login.html"):
    if request.method == 'POST':
        if request.POST['type'] == 'register':
            register_form = RegisterationForm(request.POST)
            login_form = AuthenticationForm()
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.email = register_form.cleaned_data.get('email')
                user.save()
                profile = Profile.objects.create(user=user)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login_func(request, user)
                return redirect('home')
        else:
            login_form = AuthenticationForm(data=request.POST)
            register_form = RegisterationForm()
            if login_form.is_valid():
                login_func(request, login_form.get_user())
                return redirect('home')
    else:
        register_form = RegisterationForm()
        login_form = AuthenticationForm()

    ctx = {
        'register_form': register_form,
        'login_form': login_form,
    }

    return render(request, template, ctx)


def logout(request):
    logout_func(request)
    return redirect('home')