# Create your views here.

#import Django stuff
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, Count, Sum
from django.core.exceptions import ObjectDoesNotExist

#import models
from transactions.models import Transaction, Income, Expenditure, IncomeCategory, ExpenditureCategory
from transactions.models import ExpenditureForm, IncomeForm

from budget.models import Budget
from positions.models import Position



def index(request):
#================================================================================
# index
#================================================================================
    template = dict()
    
    return render_to_response('transactions/index.htm',template, context_instance=RequestContext(request))


def create_transaction(request):
#================================================================================
# create transaction page
#================================================================================
    template = dict()
    
    types = []
    
    types.append('Income')
    types.append('Expenditure')

    template['types'] = types

    return render_to_response('transactions/create_transaction.htm', template, context_instance=RequestContext(request))    


def create_income(request):
#================================================================================
# create income object
#================================================================================
    #dictionary that passes information to the template
    template = dict()

    # If the form has been submitted
    if request.method == 'POST': 
        form = IncomeForm(request.POST)

        #validate fields
        if form.is_valid(): # check if fields validated
            item = form.cleaned_data
            item = form.save(commit=False)
            item.budget = Budget.objects.get(term=item.term, year=item.year, position=item.position)
            item.type = "IN"
            form.save()
            return HttpResponseRedirect(reverse('transaction_confirm_transaction', kwargs={'id': item.id}))
            
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
            item = form.cleaned_data
            item = form.save(commit=False)
            item.budget = Budget.objects.get(term=item.term, year=item.year, position=item.position)
            item.type = "EX"
            form.save()
            return HttpResponseRedirect(reverse('transaction_confirm_transaction', kwargs={'id': item.id}))
        
    
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
        
                return HttpResponseRedirect(reverse('transaction_confirm_transaction', kwargs={'id': item.id})) # Redirect after POST
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
        
                return HttpResponseRedirect(reverse('transaction_confirm_transaction', kwargs={'id': item.id})) # Redirect after POST
                         
        else:
            form = ExpenditureForm(instance=t)
                    
    template["t"] = t
    template["form"] = form #pass the form to template as "form" variable
       
    return render_to_response('transactions/edit_transaction.htm', template, context_instance=RequestContext(request))

def view_transactions(request, year=None, term=None):
#================================================================================
# view all transactions
#================================================================================
    template = dict()
    expenditures = Expenditure.objects.all()
    incomes = Income.objects.all()
    transactions = Transaction.objects.all()
    
    terms = []
    terms.append('S')
    terms.append('W')
    terms.append('F')
    template['terms'] = terms
    
    years_list = transactions.values('year').distinct().order_by()
    years =[]
    count = 0
    for y in years_list:
        years.append(y['year'])
        
    
    template['years'] = years
    template['all'] = "all"
    
    
    if year:
        incomes = incomes.filter(year=year)
        expenditures = expenditures.filter(year=year)
        template['year'] = int(year)
    if term:
        incomes = incomes.filter(term=term)
        expenditures = expenditures.filter(term=term)
        template['term'] = term    
   
    
    template['incomes'] = incomes
    template['expenditures'] = expenditures
    
    expenditures_total = expenditures.aggregate(total=Sum('amount'))
    incomes_total = incomes.aggregate(total=Sum('amount'))
    
    #save variables to be passed into the template for use there
    template['expenditures'] = expenditures
    template['expenditures_total'] = expenditures_total
    template['incomes_total'] = incomes_total
    template['incomes'] = incomes

    
    
    return render_to_response('transactions/view_transactions.htm', template, context_instance=RequestContext(request))


def delete_transaction(request, id):
#===============================================================================
# DELETE transactions
#===============================================================================
    template = dict()
    
    t = Transaction.objects.get(pk=id)
    if t.approved == False:
        t.delete()
        delete = True
                  
    template["confirm"] = True
    template["trans"] = t
    template["delete"] = delete
    
    return HttpResponseRedirect (reverse('transaction_view_transactions')) #redirect to list of transactions after delete is complete


def confirm_delete_transaction(request, id):
#===============================================================================
# DELETE transactions
#===============================================================================

    template = dict()
    
    t = Transaction.objects.get(pk=id)

    if t.approved == False:
        template["permission"] = True

 
    template["trans"] = t

    return render_to_response('transactions/confirm_delete_transaction.htm', template, context_instance=RequestContext(request))


def view_transaction(request, id):
#===============================================================================
# View details of transaction
#===============================================================================
    template = dict()
    
    t = Transaction.objects.get(pk=id)
    if t.type == "IN":
        t = Income.objects.get(pk=id)
    else:
        t = Expenditure.objects.get(pk=id)
        
    template["t"] = t
    return render_to_response('transactions/view_transaction.htm', template, context_instance=RequestContext(request))

def confirm_transaction(request, id):
#===============================================================================
# View details of transaction
#===============================================================================
    template = dict()
    
    t = Transaction.objects.get(pk=id)
    if t.type == "IN":
        t = Income.objects.get(pk=id)
    else:
        t = Expenditure.objects.get(pk=id)
        if not t.reciept_img:
            template["no_receipt"] = True
        
    template["t"] = t
    return render_to_response('transactions/confirm_transaction.htm', template, context_instance=RequestContext(request))


def approved_switch(request, id):
    
    transaction = Transaction.objects.get(pk=id)
   
    if(transaction.approved == True):
        transaction.approved = False
        transaction.save()
    else:
        transaction.approved = True
        transaction.save()

    return HttpResponseRedirect(reverse('transaction_view_transactions') )
    
