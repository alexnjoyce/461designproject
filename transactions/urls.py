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
    
    
    url(r'^transaction/create/transaction/$',                'create_transaction',                name="transaction_create_transaction"),
    url(r'^transaction/create/income/$',                'create_income',                name="transaction_create_income"),
    url(r'^transaction/create/expenditure/$',           'create_expenditure',           name="transaction_create_expenditure"),
    url(r'^transaction/(?P<id>\d+)/confirm/$',           'confirm_transaction',           name="transaction_confirm_transaction"),
    
    url(r'^transaction/view/$',                         'view_transactions',                     name="transaction_view_transactions"),
    url(r'^transaction/view/(?P<year>\d{4})/$',           'view_transactions',                         name="transaction_view_transactions"),
    url(r'^transaction/view/(?P<term>\w{1})/$',           'view_transactions',                         name="transaction_view_transactions"),
    url(r'^transaction/view/(?P<year>\d{4})/(?P<term>\w{1})/$', 'view_transactions',                         name="transaction_view_transactions"),
    url(r'^transaction/view/(?P<account>\w{7})/$',          'view_transactions',                         name="transaction_view_transactions"), 
    
    
    url(r'^transaction/details/(?P<id>\d+)/$',             'view_transaction',                     name="transaction_view_transaction"),
    url(r'^transaction/edit/income/(?P<id>\d+)/$',             'edit_income',             name="transaction_edit_income"),
    url(r'^transaction/edit/expenditure/(?P<id>\d+)/$',             'edit_expenditure',             name="transaction_edit_expenditure"),
    url(r'^transaction/confirm/delete/(?P<id>\d+)/$',       'confirm_delete_transaction',   name="transaction_confirm_delete_transaction"),
    url(r'^transaction/delete/(?P<id>\d+)/$',           'delete_transaction',           name="transaction_delete_transaction"),
    
    url(r'^transaction/(?P<id>\d+)/approve/$',              'approved_switch',                       name="transaction_approved_switch"),
    url(r'^transaction/(?P<id>\d+)/chequeready/$',          'ready_switch',                       name="transaction_ready_switch"),
    url(r'^transaction/(?P<id>\d+)/chequereceived/$',          'received_switch',                       name="transaction_received_switch"),
    url(r'^transaction/upload/$',                         'upload_data',                       name="transaction_upload_transaction"),

)