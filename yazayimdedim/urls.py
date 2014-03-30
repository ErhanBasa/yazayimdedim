from django.conf.urls import patterns, include, url
from blog.views import articles, article, sitemap, LatestArticlesFeed, contact, profile, login
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yazayimdedim.views.home', name='home'),
    # url(r'^yazayimdedim/', include('yazayimdedim.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
 	url(r'^$', articles),
 	url(r'^giris/$', login, name='login'),
 	url(r'^iletisim/$', contact, name='contact'),
 	url(r'^(?P<slug>[\w-]+)/$', article),
 	url(r'^ckeditor/', include('ckeditor.urls')),
 	url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
 	url(r'^sitemap.xml', sitemap),
 	url(r'^latest/feed/$', LatestArticlesFeed()),
 	url(r'^yazar/(?P<slug>[\w.@+-]+)/$', profile),
)
