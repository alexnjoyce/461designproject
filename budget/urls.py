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
urlpatterns += patterns('budget.views',
    
    url(r'^budget/create/$',                        'create_budget',                        name="budget_create_budget"),
    url(r'^budget/(?P<id>\d+)/items/create/$',       'create_budgetitems',                        name="budget_create_budgetitems"),
    url(r'^budget/(?P<id>\d+)/confirm/$',       'confirm_budgetitems',                        name="budget_confirm_budgetitems"),
    
       url(r'^budget/(?P<id>\d+)/delete/$',       'delete_budget',                        name="budget_delete_budget"),
    
    url(r'^budgets/view/$',                          'view_budgets',                         name="budget_view_budgets"),
    url(r'^budgets/view/(?P<year>\d{4})/$',           'view_budgets',                         name="budget_view_budgets"),
    url(r'^budgets/view/(?P<account>\w{7})/$',           'view_budgets',                         name="budget_view_budgets"),
    url(r'^budgets/view/(?P<term>\w{1})/$',           'view_budgets',                         name="budget_view_budgets"),
    url(r'^budgets/view/(?P<year>\d{4})/(?P<term>\w{1})/$', 'view_budgets',                         name="budget_view_budgets"),
    
    url(r'^budget/edit/(?P<id>\d+)/$',              'edit_budgetitems',                         name="budget_edit_budgetitems"),
    
    url(r'^budget/(?P<id>\d+)/approve/$',            'approved_switch',                       name="budget_approved_switch"),
    url(r'^budget/(?P<id>\d+)/view/$',              'view_budgetitems',                         name="budget_view_budgetitems"),
    
    url(r'^budget/upload/$',                         'upload_data_budget',                       name="budget_upload_budget"),
    url(r'^budget/items/upload/$',                         'upload_data_budgetitems',                       name="budget_upload_budgetitems"),


)