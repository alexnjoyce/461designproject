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
urlpatterns += patterns('categories.views',
    
    url(r'^create/category/$',                         'create_category',                       name="category_create_category"),
    url(r'^create/category/(?P<type>\w+)/$',          'create_category',                        name="category_create_category"),
    url(r'^create/category/confirm/(?P<id>\d+)/$',    'create_confirmation',                    name="category_create_confirm"),
    
    url(r'^category/delete/(?P<id>\d+)/$',        'delete_category',                        name="category_delete_category"),
    
    url(r'^view/category/$',                           'view_categories',                       name="category_view_categories"),
    url(r'^view/category/(?P<criteria>\w+)/$',        'view_categories',                        name="category_view_categories"),
    
    url(r'^category/switch/(?P<state>\w+)/(?P<id>\d+)/$',            'isactive_switch',         name="category_isactive_switch"),

)