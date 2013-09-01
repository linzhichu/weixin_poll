from django.conf.urls import patterns, include, url
from views import home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$',home),
    url(r'^weixin/$',handleRequest),
    # Examples:
    # url(r'^$', 'th_back.views.home', name='home'),
    # url(r'^th_back/', include('th_back.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
