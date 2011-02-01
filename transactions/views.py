# Create your views here.

#import Django stuff
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, Count, Sum

#import models
from transactions.models import Transaction, Income, Expenditure, IncomeCategory, ExpenditureCategory
from transactions.models import ExpenditureForm, IncomeForm



def index(request):
#================================================================================
# index
#================================================================================
    template = dict()
    
    return render_to_response('transactions/index.htm',template, context_instance=RequestContext(request))


def create_income(request):
#================================================================================
# create income object
#================================================================================
    #dictionary that passes information to the template
    template = dict()
    template['test'] = "does this work?!!?!"
    template['test2'] = "does this REALLY work?!!?!"
    # If the form has been submitted
    if request.method == 'POST': 
        form = IncomeForm(request.POST)

        #validate fields
        if form.is_valid(): # check if fields validated
            cleaned_data = form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('index'))
            
    #else blank form   
    else:
        form = IncomeForm()

    template['form'] = form
    
    #tells the view which template to use, and to pass the template dictionary
    return render_to_response('transactions/create_income.htm',template, context_instance=RequestContext(request))

def create_expenditure(request):
#================================================================================
# create expenditure object
#================================================================================
    template = dict()
    
    # If the form has been submitted
    if request.method == 'POST': 
        form = ExpenditureForm(request.POST)

        #validate fields
        if form.is_valid(): # check if fields validated
            cleaned_data = form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('index'))
        
    
    #else blank form   
    else:
        form = ExpenditureForm()

    template['form'] = form
    
    
    return render_to_response('transactions/create_expenditure.htm',template, context_instance=RequestContext(request))


def edit_transaction(request, id):
#================================================================================
# edit specific transaction - general
#================================================================================
    template = dict()
    t = Transaction.objects.get(pk=id)
    type = t.type
    
#    if income, then use all Income forms
    if t.type == "IN":
        t = get_object_or_404(Income, pk=id)
        if request.method == 'POST': # If the form has been submitted...    
            form = IncomeForm(request.POST, instance=t)   
           
            #validate fields
            if form.is_valid(): # check if fields validated
                cleaned_data = form.cleaned_data
                form = form.save(commit=False) #save it to the db
                #.editor = request.user
                form.save()
        
                return HttpResponseRedirect(reverse('index')) # Redirect after POST
        else:
            form = IncomeForm(instance=t)
                
#    if expenditure then use expenditure forms
    else:
        t = get_object_or_404(Expenditure, pk=id)
        if request.method == 'POST': # If the form has been submitted...
            form = ExpenditureForm(request.POST, instance=t) 
            
#            validate fields
            if form.is_valid(): # check if fields validated
                cleaned_data = form.cleaned_data
                form = form.save(commit=False) #save it to the db 
                form.editor = request.user
                form.save()
        
                return HttpResponseRedirect(reverse('index')) # Redirect after POST
                         
        else:
            form = ExpenditureForm(instance=t)
                    
    template["t"] = t
    template["form"] = form #pass the form to template as "form" variable
       
    return render_to_response('transactions/edit_transaction.htm', template, context_instance=RequestContext(request))

def view_all(request):
#================================================================================
# view all transactions
#================================================================================
    template = dict()
    
    #get all the transactions
    expenditures = Expenditure.objects.all()
    incomes = Income.objects.all()
    
    expenditures_total = expenditures.aggregate(total=Sum('amount'))
    incomes_total = incomes.aggregate(total=Sum('amount'))
    
    #save variables to be passed into the template for use there
    template['expenditures'] = expenditures
    template['expenditures_total'] = expenditures_total
    template['incomes_total'] = incomes_total
    template['incomes'] = incomes

    
    
    return render_to_response('transactions/view_all.htm', template, context_instance=RequestContext(request))


def delete_transaction(request, id):
#===============================================================================
# DELETE transactions
#===============================================================================
    template = dict()
    
    t = Transaction.objects.get(pk=id)
    t.delete()
    permission = True
    delete = True
                  
    template["confirm"] = True
    template["trans"] = t
    template["permission"] = permission
    template["delete"] = delete
    
    return HttpResponseRedirect (reverse('view_all')) #redirect to list of transactions after delete is complete


def confirm_delete_transaction(request, id):
#===============================================================================
# DELETE transactions
#===============================================================================

    template = dict()
    
    t = Transaction.objects.get(pk=id)
 
    template["trans"] = t

    return render_to_response('transactions/confirm_delete_transaction.htm', template, context_instance=RequestContext(request))
