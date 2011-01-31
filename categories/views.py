from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from categories.models import Category, IncomeCategory, ExpenditureCategory, IncomeCategoryForm, ExpenditureCategoryForm


def create_category(request, type):
    template = dict()
    
#    if you want to make income category
    if type == "income":
    #   if the form has been submitted
        if request.method == 'POST': 
            form = IncomeCategoryForm(request.POST)
    
            #validate fields
            if form.is_valid(): # check if fields validated
                cleaned_data = form.cleaned_data
                form.save()
                return HttpResponseRedirect(reverse('category_view_categories', kwargs={'criteria': "all"}))
    
                
        #else blank form   
        else:
            form = IncomeCategoryForm()
            
#    else type is expenditure
    else:
        #   if the form has been submitted
        if request.method == 'POST': 
            form = ExpenditureCategoryForm(request.POST)
    
            #validate fields
            if form.is_valid(): # check if fields validated
                cleaned_data = form.cleaned_data
                form.save()
                return HttpResponseRedirect(reverse('category_view_categories', kwargs={'criteria': "all"}))
    
                
        #else blank form   
        else:
            form = ExpenditureCategoryForm()

    template['form'] = form
    template['type'] = type
    
    #tells the view which template to use, and to pass the template dictionary
    return render_to_response('categories/create_category.htm',template, context_instance=RequestContext(request))

def view_categories(request, criteria):
    template = dict()
    
    if criteria == 'all':
        income_categories = IncomeCategory.objects.all()
        expenditure_categories = ExpenditureCategory.objects.all()
    elif criteria == 'active':
        income_categories = IncomeCategory.objects.filter(isactive=True)
        expenditure_categories = ExpenditureCategory.objects.filter(isactive=True)
    elif criteria == 'inactive':
        income_categories = IncomeCategory.objects.filter(isactive=False)
        expenditure_categories = ExpenditureCategory.objects.filter(isactive=False)
    
    template['income_categories'] = income_categories
    template['expenditure_categories'] = expenditure_categories
    template['criteria'] = criteria
    
    return render_to_response('categories/view_categories.htm',template, context_instance=RequestContext(request))

def isactive_switch(request, state, id):
    
    category = Category.objects.get(pk=id)
   
    if(category.isactive == True):
        category.isactive = False
        category.save()
    else:
        category.isactive = True
        category.save()
    
    criteria = state

    return HttpResponseRedirect(reverse('category_view_categories', kwargs={'criteria': criteria}) )

    