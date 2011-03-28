# Create your views here.
import csv
import datetime

#import Django stuff
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, Count, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

#helper functions
from overall.views import is_admin, is_vpf

#import models
from transactions.models import Transaction, Income, Expenditure, IncomeCategory, ExpenditureCategory
from transactions.models import ExpenditureForm, IncomeForm, UploadDataForm
from settings import MEDIA_ROOT

from budget.models import Budget
from positions.models import Position



@login_required
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

@login_required
def create_income(request):
#================================================================================
# create income object
#================================================================================
    #dictionary that passes information to the template
    template = dict()

    # If the form has been submitted
    if request.method == 'POST': 
        form = IncomeForm(request.POST, request.FILES)

        #validate fields
        if form.is_valid(): # check if fields validated
            item = form.cleaned_data
            item = form.save(commit=False)
            item.budget = Budget.objects.get(term=item.term, year=item.year, position=item.position)
            item.type = "IN"
            item.creator = request.user
            form.save()
            return HttpResponseRedirect(reverse('transaction_confirm_transaction', kwargs={'id': item.id}))
            
    #else blank form   
    else:
        form = IncomeForm()

    template['form'] = form
    
    #tells the view which template to use, and to pass the template dictionary
    return render_to_response('transactions/create_income.htm',template, context_instance=RequestContext(request))

@login_required
def create_expenditure(request):
#================================================================================
# create expenditure object
#================================================================================
    template = dict()
    
    # If the form has been submitted
    if request.method == 'POST': 
        form = ExpenditureForm(request.POST, request.FILES)

        #validate fields
        if form.is_valid(): # check if fields validated
            item = form.cleaned_data
            item = form.save(commit=False)
            item.budget = Budget.objects.get(term=item.term, year=item.year, position=item.position)
            item.type = "EX"
            item.creator = request.user
            form.save()
            return HttpResponseRedirect(reverse('transaction_confirm_transaction', kwargs={'id': item.id}))
        
    
    #else blank form   
    else:
        form = ExpenditureForm()

    template['form'] = form
    
    
    return render_to_response('transactions/create_expenditure.htm',template, context_instance=RequestContext(request))

@login_required
def edit_income(request, id):
#================================================================================
# edit specific transaction - general
#================================================================================
    template = dict()

    
    t = get_object_or_404(Income, pk=id)
    if request.method == 'POST': # If the form has been submitted...    
        form = IncomeForm(request.POST, instance=t)   
       
        #validate fields
        if form.is_valid(): # check if fields validated
            cleaned_data = form.cleaned_data
            form = form.save(commit=False) #save it to the db
            #.editor = request.user
            form.save()
    
            return HttpResponseRedirect(reverse('transaction_confirm_transaction', kwargs={'id': form.id})) # Redirect after POST
    else:
        form = IncomeForm(instance=t)
                
 
    template["t"] = t
    template["form"] = form #pass the form to template as "form" variable
       
    return render_to_response('transactions/edit_income.htm', template, context_instance=RequestContext(request))

@login_required
def edit_expenditure(request, id):
#================================================================================
# edit specific transaction - general
#================================================================================
    template = dict()

    t = get_object_or_404(Expenditure, pk=id)
    if request.method == 'POST': # If the form has been submitted...
        form = ExpenditureForm(request.POST, instance=t) 
        
#            validate fields
        if form.is_valid(): # check if fields validated
            cleaned_data = form.cleaned_data
            form = form.save(commit=False) #save it to the db 
            #form.editor = request.user
            form.save()
    
            return HttpResponseRedirect(reverse('transaction_confirm_transaction', kwargs={'id': form.id})) # Redirect after POST
                     
    else:
        form = ExpenditureForm(instance=t)
    
    template["t"] = t
    template["form"] = form #pass the form to template as "form" variable    

    return render_to_response('transactions/edit_expenditure.htm', template, context_instance=RequestContext(request))    

@login_required
def view_transactions(request, year=None, term=None, account=None):
#================================================================================
# view all transactions
#================================================================================
    template = dict()
    
    expenditures = Expenditure.objects.all()
    incomes = Income.objects.all()
    transactions = Transaction.objects.all()
    
    if not account:
        if not is_admin(request.user):
            expenditures = expenditures.filter(approved=True)
            incomes = incomes.filter(approved=True)
            transactions = transactions.filter(approved=True)
    else:
        if is_admin(request.user):
            expenditures = expenditures.filter(approved=False)
            incomes = incomes.filter(approved=False)
            transactions = transactions.filter(approved=False)  
        else:
            expenditures = expenditures.filter(creator=request.user)
            incomes = incomes.filter(creator=request.user)
            transactions = transactions.filter(creator=request.user)           
        
    
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
    template['transactions'] = transactions
    
    expenditures_total = expenditures.aggregate(total=Sum('amount'))
    incomes_total = incomes.aggregate(total=Sum('amount'))
    
    #save variables to be passed into the template for use there
    template['expenditures'] = expenditures
    template['expenditures_total'] = expenditures_total
    template['incomes_total'] = incomes_total
    template['incomes'] = incomes
    
    template['account'] = account

    
    
    return render_to_response('transactions/view_transactions.htm', template, context_instance=RequestContext(request))

@login_required
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

@login_required
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

@login_required
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

@login_required
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
        if not t.receipt_img:
            template["no_receipt"] = True
        
    template["t"] = t
    return render_to_response('transactions/confirm_transaction.htm', template, context_instance=RequestContext(request))

@login_required
def approved_switch(request, id):
    
    transaction = Transaction.objects.get(pk=id)
   
    if(transaction.approved == True):
        transaction.approved = False
        transaction.save()
    else:
        transaction.approved = True
        transaction.save()

    return HttpResponseRedirect(reverse('transaction_view_transactions') )
    
@login_required
def upload_data(request):
    
    template = dict()
    
    if request.method == 'POST':
        
        form = UploadDataForm(request.POST, request.FILES)
        if form.is_valid():             
            
            directory = MEDIA_ROOT + "/test_data/" + request.FILES["file"].name
            
            reader = csv.reader(open(directory))
            
            for r in reader:
                if r[0] == "IN":
                    item = Income()
                    item.type = "IN"
                    item.name = r[1]
                    item.email = r[2]
                    item.date = datetime.date(year=int(r[3]), month=int(r[4]), day=int(r[5]))
                    item.amount = r[6]
                    item.description = r[7]
                    if r[8] == "TRUE":
                        item.approved = True
                    if r[9] == "TRUE":
                        item.cheque_ready = True
                    if r[10] == "TRUE":
                        item.cheque_received = True
                    item.term = r[11]
                    item.year = r[12]
                    item.position = Position.objects.get(name=r[13])                
                    item.budget = Budget.objects.get(position__name=r[13],term=r[11],year=r[12])
                    item.income_category = IncomeCategory.objects.get(name=r[14])
                    item.creator = request.user
                    item.save()
                elif r[0] == "EX":
                    item = Expenditure()
                    item.type = "EX"
                    item.name = r[1]
                    item.email = r[2]
                    item.date = datetime.date(year=int(r[3]), month=int(r[4]), day=int(r[5]))
                    item.amount = r[6]
                    item.description = r[7]
                    if r[8] == "TRUE":
                        item.approved = True
                    if r[9] == "TRUE":
                        item.cheque_ready = True
                    if r[10] == "TRUE":
                        item.cheque_received = True
                    item.cheque_ready = r[9]
                    item.cheque_received = r[10]
                    item.term = r[11]
                    item.year = r[12]
                    item.position = Position.objects.get(name=r[13])                
                    item.budget = Budget.objects.get(position__name=r[13],term=r[11],year=r[12])
                    item.expenditure_category = ExpenditureCategory.objects.get(name=r[14])
                    item.hst = r[15]
                    item.creator = request.user
                    item.save()
                    
        return HttpResponseRedirect(reverse('transaction_view_transactions'))
    else:
        form = UploadDataForm()
    
    template['form'] = form
    
    return render_to_response('transactions/upload_transactions.htm',template, context_instance=RequestContext(request))  