from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^syde461/', include('syde461.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    
)


#include file by file for each of the url.py files in the app folders
urlpatterns += patterns('',
    (r'', include('positions.urls')),
    (r'', include('budget.urls')),
    (r'', include('categories.urls')),
    (r'', include('transactions.urls')),
    (r'', include('overall.urls')),
    

)