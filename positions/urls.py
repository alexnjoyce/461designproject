from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

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
urlpatterns += patterns('positions.views',
    
    url(r'^create/position/$',                        'create_position',                        name="position_create_position"),
#    url(r'^create/position/success/$',                'create_position_success',                name="create_position_success"),
    url(r'^view/position/$',                          'view_positions',                         name="position_view_positions"),
    url(r'^view/position/(?P<criteria>\w+)/$',        'view_positions',                         name="position_view_positions"),
    url(r'^position/switch/(?P<state>\w+)/(?P<id>\d+)/$',            'isactive_switch',                       name="position_isactive_switch"),

    url(r'^upload/positions/$',                         'upload_data',                       name="position_upload_positions"),
)


urlpatterns += patterns('',
        (r'^media_site/(?P<path>.*)$', 'django.views.static.serve', {'document_root':     settings.MEDIA_ROOT}),
)