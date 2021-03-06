from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import csv

from categories.models import Category, IncomeCategory, ExpenditureCategory, IncomeCategoryForm, ExpenditureCategoryForm, UploadDataForm
from transactions.models import Income, Expenditure
from settings import MEDIA_ROOT

@login_required
def create_category(request, type=None):
    template = dict()
                    
    types = []

    types.append('income')
    types.append('expenditure')

    template['types'] = types
    
    
#    if you want to make income category
    if type == "income":
    #   if the form has been submitted
        if request.method == 'POST': 
            form = IncomeCategoryForm(request.POST)
    
            #validate fields
            if form.is_valid(): # check if fields validated
                cleaned_data = form.cleaned_data
                category = form.save()
                return HttpResponseRedirect(reverse('category_create_confirm', kwargs={'id': category.id}))
    
                
        #else blank form   
        else:
            form = IncomeCategoryForm()
        template['form'] = form
            
#    else type is expenditure
    elif type == "expenditure":
        #   if the form has been submitted
        if request.method == 'POST': 
            form = ExpenditureCategoryForm(request.POST)
    
            #validate fields
            if form.is_valid(): # check if fields validated
                cleaned_data = form.cleaned_data
                category = form.save()
                
                return HttpResponseRedirect(reverse('category_create_confirm', kwargs={'id': category.id}))
    
                
        #else blank form   
        else:
            form = ExpenditureCategoryForm()
        template['form'] = form
    
    template['type'] = type
    
    #tells the view which template to use, and to pass the template dictionary
    return render_to_response('categories/create_category.htm',template, context_instance=RequestContext(request))

@login_required
def create_confirmation (request, id):
    template = dict()
    
    category = get_object_or_404(Category, pk=id)
    
    template['category'] = category
    
    return render_to_response('categories/confirm.htm',template, context_instance=RequestContext(request))

@login_required
def delete_category(request, id):
#===============================================================================
# DELETE category
#===============================================================================
    template = dict()
    
    category = get_object_or_404(Category, pk=id)
    transactions_in = Income.objects.filter(income_category=category) 
    transactions_ex = Expenditure.objects.filter(expenditure_category=category)
                  
    if not transactions_in or not transactions_ex:
        category.delete()
        delete = True
    else:
        delete = False
    
    template["category"] = category
    template["delete"] = delete
    
    return render_to_response('categories/delete.htm',template, context_instance=RequestContext(request))


@login_required
def view_categories(request, criteria=None):
    template = dict()
    
    criteria_list = []
    criteria_list.append('active')
    criteria_list.append('inactive')
    
    template['criteria_list'] = criteria_list
    
    if criteria == 'active':
        income_categories = IncomeCategory.objects.filter(isactive=True)
        expenditure_categories = ExpenditureCategory.objects.filter(isactive=True)
    elif criteria == 'inactive':
        income_categories = IncomeCategory.objects.filter(isactive=False)
        expenditure_categories = ExpenditureCategory.objects.filter(isactive=False)
    else:
        income_categories = IncomeCategory.objects.all()
        expenditure_categories = ExpenditureCategory.objects.all()
    
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

@login_required
def upload_data(request):
    
    template = dict()
    
    if request.method == 'POST':
        
        form = UploadDataForm(request.POST, request.FILES)
        if form.is_valid():             
            
            directory = MEDIA_ROOT + "/test_data/" + request.FILES["file"].name
            
            reader = csv.reader(open(directory))
            
            for r in reader:
                if r[0] == "EX":
                    category = ExpenditureCategory()
                    category.name = r[1]
                    category.isactive = True
                    category.save()
                elif r[0] == "IN":
                    category = IncomeCategory()
                    category.name = r[1]
                    category.isactive = True
                    category.save()
            
        return HttpResponseRedirect(reverse('category_view_categories'))
    else:
        form = UploadDataForm()
    
    template['form'] = form
    
    return render_to_response('categories/upload_categories.htm',template, context_instance=RequestContext(request))    
    
