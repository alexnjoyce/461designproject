from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^syde461/', include('syde461.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    
)

#all our url patterns go here
urlpatterns += patterns('transactions.views',
    
    url(r'^$','index', name="index"),
    url(r'^create/income/$',                'create_income',                name="create_income"),
    url(r'^create/expenditure/$',           'create_expenditure',           name="create_expenditure"),
    url(r'^view/$',                         'view_all',                     name="view_all"),
    url(r'^edit/(?P<id>\d+)/$',             'edit_transaction',             name="edit_transaction"),
    url(r'^confdelete/(?P<id>\d+)/$',       'confirm_delete_transaction',   name="confirm_delete_transaction"),
    url(r'^delete/(?P<id>\d+)/$',           'delete_transaction',           name="delete_transaction"),

)

#include file by file for each of the url.py files in the app folders
urlpatterns += patterns('',
    (r'', include('positions.urls')),
    (r'', include('budget.urls')),
    (r'', include('categories.urls')),
    

)