# -*- coding: utf-8 -*-

from blog.models import Tag, Category, Post
from django.shortcuts import render,get_object_or_404
from django.contrib.syndication.views import Feed
from blog.forms import ContactForm
from django.contrib import messages

def articles(request, template = 'index.html'):
	tags = Tag.objects.all().order_by('name')
	categories = Category.objects.all().order_by('name')
	posts = Post.objects.all().order_by('-date')

	ctx = {
		'tags': tags,
		'categories': categories,
		'posts': posts,
	}

	return render(request,template,ctx)

def article(request, slug, template = 'post.html'):
	categories = Category.objects.all().order_by('name')
	tags = Tag.objects.all().order_by('name')
	post = get_object_or_404(Post, slug=slug)
	posts = Post.objects.all().exclude(pk=post.pk).order_by('?')[:6]
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

	return render(request,template,ctx)



def sitemap(request, template="sitemap.html"):
	posts = Post.objects.all().order_by('-date')

	ctx = {
		'posts' : posts,
	}
	
	return render(request,template,ctx)

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

	def item_link(self,item):
		return item.get_absolute_url()

def contact(request, template="contact.html"):
    if request.method=='POST':
            form=ContactForm(request.POST)
            if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.SUCCESS, u'Tamamdır')
                    form=ContactForm()
    else:
            form=ContactForm()
    ctx = {
            'form' : form,
    }
    return render(request,template,ctx)