from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'friendzy.views.home', name='home'),
    # url(r'^friendzy/', include('friendzy.foo.urls')),
    url(r'login', 'users.views.login'),
    url(r'set_status', 'users.views.set_status'),
    url(r'match', 'users.views.match'),
    url(r'resetFixture', 'users.views.TESTAPI_resetFixture'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'', include('gcm.urls')),
    url(r'gcmtest', 'users.views.gcmtest'),
)
