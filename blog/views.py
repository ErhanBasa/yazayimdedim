# -*- coding: utf-8 -*-
from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as login_func, authenticate, logout as logout_func
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blog.models import Tag, Category, Post, Profile
from blog.forms import ContactForm, RegisterationForm, LoginForm as AuthenticationForm, ProfileForm, ArticleForm
from blog.utils import get_count, send_mail_with_template


def articles(request, template='index.html'):
    tags = Tag.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    posts = Post.objects.filter(is_active=True).order_by('-date')
    last_post = posts[0] if posts else None
    if last_post:
        last_post_uri = request.build_absolute_uri(reverse('detail', args=(last_post.slug, )))
        last_post_facebook_count = get_count('facebook', last_post_uri)
        last_post_twitter_count = get_count('twitter', last_post_uri)
    else:
        last_post_facebook_count = None
        last_post_twitter_count = None
    return render(request, template, {
        'tags': tags,
        'categories': categories,
        'posts': posts,
        'last_post': last_post,
        'last_post_facebook_count': last_post_facebook_count,
        'last_post_twitter_count': last_post_twitter_count
    })


def article(request, slug, template='post.html'):
    categories = Category.objects.all().order_by('name')
    tags = Tag.objects.all().order_by('name')
    post = get_object_or_404(Post.objects.select_related('user'), slug=slug)
    if not post.is_active and post.user != request.user:
        if not request.user.is_staff:
            raise Http404
    posts = Post.objects.all().exclude(pk=post.pk).order_by('?')[:3]
    category = post.category.all()
    tag = post.tag.all()
    uri = request.build_absolute_uri()
    is_editable = post.user == request.user
    return render(request, template, {
        'facebook_count': get_count('facebook', uri),
        'twitter_count': get_count('twitter', uri),
        'categories': categories,
        'category': category,
        'posts': posts,
        'post': post,
        'tags': tags,
        'tag': tag,
        'is_editable': is_editable,
    })


def sitemap(request, template="sitemap.html"):
    posts = Post.objects.filter(is_active=True).order_by('-date')

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
                    contact = form.save()
                    send_mail_with_template(u'Yeni iletişim maili', settings.MY_MAIL, 
                        'mails/newmessage.html', {'contact': contact})
                    messages.add_message(request, messages.SUCCESS, u'Tamamdır')
                    return redirect('contact')
    else:
            form = ContactForm()
    ctx = {
        'form': form,
    }
    return render(request, template, ctx)


def profile(request, slug, template="profile.html"):
    profile = get_object_or_404(Profile, user__username__iexact=slug)
    posts = Post.objects.filter(user=profile.user).order_by("-date")
    is_editable = request.user == profile.user

    if request.method == 'POST':
        profileform = ProfileForm(instance=profile, data=request.POST, files=request.FILES)
        if profileform.is_valid():
            profileform.save()
            return redirect('profile', slug)
    else:
        profileform = ProfileForm(instance=profile)

    ctx = {
        'profile': profile,
        'posts': posts,
        'profileform': profileform,
        'is_editable': is_editable
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
                send_mail_with_template(u'Selamlar efendim!', user.email, 
                        'mails/wellcome.html', {'user': user})
                send_mail_with_template(u'Yeni üye kaydı!', settings.MY_MAIL,
                        'mails/wellcome.html', {'user': user})
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


@login_required
def logout(request):
    logout_func(request)
    return redirect('home')


@login_required
def create_post(request, template="create_post.html"):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.date = date.today()
            post.is_active = False
            post.save()
            send_mail_with_template(u'Yeni yazı var', settings.MY_MAIL, 
                        'mails/newpost.html', {'post': post, 'user': request.user})
            return redirect('detail', post.slug)
    else:
        form = ArticleForm()
    return render(request, template, {'form': form})


@login_required
def update_post(request, slug, template="create_post.html"):
    post = get_object_or_404(Post.objects.select_related('user'), slug=slug)
    if post.user != request.user:
        raise Http404
    if request.method == 'POST':
        form = ArticleForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('detail', post.slug)
    else:
        form = ArticleForm(instance=post)
    return render(request, template, {'form': form, 'is_deletable': True, 'slug': slug})


@login_required
def delete_post(request, slug, template="create_post.html"):
    post = get_object_or_404(Post.objects.select_related('user'), slug=slug)
    if post.user != request.user:
        raise Http404
    post.delete()
    return redirect('home')
