#python functionality
import datetime


#django functionality
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, Count, Sum
from django.forms.formsets import formset_factory



from positions.models import Position
from budget.models import Budget, BudgetItem, BudgetItemForm, BudgetForm

def check(check):
#===============================================================================
# helper function to check for null values
#===============================================================================
    if not check:
        check = 0
    return check

def start_date(year, term):
#===============================================================================
# helper function to get start date based on term/year for budget model
#===============================================================================
    if term == 'S':
        date = datetime.date(year=year, month=5, day=1)
    elif term == 'F':
        date = datetime.date(year=year, month=9, day=1)
    elif term == 'W':
        date = datetime.date(year=year, month=1, day=1)
    
    return date

def end_date(year, term):
#===============================================================================
# helper function to get end date based on term/year for budget model
#===============================================================================
    if term == 'S':
        date = datetime.date(year=year, month=8, day=31)
    elif term == 'F':
        date = datetime.date(year=year, month=12, day=31)
    elif term == 'W':
        date = datetime.date(year=year, month=4, day=30)
    
    return date

def create_budget(request):
    template = dict()
    
#   if the form has been submitted
    if request.method == 'POST': 
        form = BudgetForm(request.POST)

        #validate fields
        if form.is_valid(): # check if fields validated
            cleaned_data = form.cleaned_data
            budget = form.save(commit=False)
            budget.creator = request.user
            budget.start_date = start_date(budget.year, budget.term)
            budget.end_date = end_date(budget.year, budget.term)
            budget.save()
            return HttpResponseRedirect(reverse('budget_create_budgetitems', kwargs={'id': budget.id}))
            
    #else blank form   
    else:
        form = BudgetForm()

    template['form'] = form
    
    #tells the view which template to use, and to pass the template dictionary
    return render_to_response('budget/create_budget.htm',template, context_instance=RequestContext(request))

def view_budgets(request, year=None, term=None):
    template = dict()
    
    budgets = Budget.objects.all()
    terms = []
    terms.append('S')
    terms.append('W')
    terms.append('F')
    template['terms'] = terms
    
    years = budgets.values('year')
    template['years'] = years
    
    if year:
        budgets = budgets.filter(year=year)
        template['year'] = year
    if term:
        budgets = budgets.filter(term=term)
        template['term'] = term
    
    
    template['budgets'] = budgets
    
    return render_to_response('budget/view_budget.htm',template, context_instance=RequestContext(request))

def create_budgetitems (request, id):
    template = dict()
    
    budget = Budget.objects.get(pk=id)
    previous_budgets = Budget.objects.filter(position=budget.position).exclude(id=budget.id)
    
    budgetFormSet = formset_factory(BudgetItemForm, extra=5)
    
    if request.method == 'POST':
        formset = budgetFormSet(request.POST)
        if formset.is_valid():
            count = 0
            for form in formset.forms:
                item = form.save(commit=False)
                if item.amount:
                    item.budget = budget
                    item.save()
            
            return HttpResponseRedirect(reverse('index'))
    
    else:
        formset = budgetFormSet()
    
    template['formset'] = formset
    template['budget'] = budget
    template['previous_budgets'] = previous_budgets
    
    return render_to_response('budget/create_budgetitems.htm',template, context_instance=RequestContext(request))

def approved_switch(request, id):
    
    budget = Budget.objects.get(pk=id)
   
    if(budget.approved == True):
        budget.approved = False
        budget.save()
    else:
        budget.approved = True
        budget.save()

    return HttpResponseRedirect(reverse('budget_view_budgets') )

def view_budgetitems (request, id):
    template = dict()
    
    budget = Budget.objects.get(pk=id)
    
    budget_items = BudgetItem.objects.filter(budget=budget)
    
    if budget_items: 
        budget_items_type = BudgetItem.objects.filter(budget=budget).values('type').annotate(sum = Sum('amount'))
        net = check(budget_items_type.get(type="IN")["sum"])-check(budget_items_type.get(type="EX")['sum'])  
        template['budget_items_type'] = budget_items_type
        template['net'] = net
    
    template['budget'] = budget
    template['budget_items'] = budget_items

    
    return render_to_response('budget/view_budgetitems.htm',template, context_instance=RequestContext(request))
                            