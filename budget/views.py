#python functionality
import datetime


#django functionality
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, Count, Sum
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory



from positions.models import Position
from budget.models import Budget, BudgetItem, IncomeBudgetItemForm, ExpenseBudgetItemForm, BudgetForm, IncomeBudgetItem, ExpenseBudgetItem

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
#===============================================================================
# make a new budget shell
#===============================================================================
    template = dict()
    
#   if the form has been submitted
    if request.method == 'POST': 
        form = BudgetForm(request.POST)

        #validate fields
        if form.is_valid(): # check if fields validated
            cleaned_data = form.cleaned_data
            budget = form.save(commit=False)
            test = Budget.objects.filter(position=budget.position, term=budget.term, year=budget.year)
            if not test:
                budget.creator = request.user
                budget.start_date = start_date(budget.year, budget.term)
                budget.end_date = end_date(budget.year, budget.term)
                budget.save()
                return HttpResponseRedirect(reverse('budget_create_budgetitems', kwargs={'id': budget.id}))
            else:
                return render_to_response('budget/create_budget_error.htm',template, context_instance=RequestContext(request))
                #budget already exists
            
            
    #else blank form   
    else:
        form = BudgetForm()

    template['form'] = form
    
    #tells the view which template to use, and to pass the template dictionary
    return render_to_response('budget/create_budget.htm',template, context_instance=RequestContext(request))

def view_budgets(request, year=None, term=None):
#===========================================================================
# view all budgets
#===========================================================================

    template = dict()
    
    budgets = Budget.objects.all()
    terms = []

    terms.append('S')
    terms.append('W')
    terms.append('F')
    template['terms'] = terms
    
    years_list = budgets.values('year').distinct().order_by()
    years =[]
    count = 0
    for y in years_list:
        years.append(y['year'])
        
    
    template['years'] = years
    template['all'] = "all"
    
    
    if year:
        budgets = budgets.filter(year=year)
        template['year'] = int(year)
    if term:
        budgets = budgets.filter(term=term)
        template['term'] = term    
   
    
    template['budgets'] = budgets
    
    return render_to_response('budget/view_budget.htm',template, context_instance=RequestContext(request))

def create_budgetitems (request, id):
#===============================================================================
# create budget items for new budgets
#===============================================================================

    template = dict()
    
    budget = Budget.objects.get(pk=id)
    previous_budgets = Budget.objects.filter(position=budget.position).exclude(id=budget.id)
    
    ExpensebudgetFormSet = formset_factory(ExpenseBudgetItemForm, extra=5)
    IncomebudgetFormSet = formset_factory(IncomeBudgetItemForm, extra=5)
    
    if request.method == 'POST':
        expense_formset = ExpensebudgetFormSet(request.POST, prefix='expenses')
        income_formset = IncomebudgetFormSet(request.POST, prefix='incomes')
        if expense_formset.is_valid()and income_formset.is_valid():
            count = 0
            for form in expense_formset.forms:
                item = form.save(commit=False)
                if item.amount:
                    item.budget = budget
                    item.type = "EX"
                    item.save()
            for form in income_formset.forms:
                item = form.save(commit=False)
                if item.amount:
                    item.budget = budget
                    item.type = "IN"
                    item.save()
            
            return HttpResponseRedirect(reverse('budget_confirm_budgetitems', kwargs={'id': budget.id}))
    
    else:
        expense_formset = ExpensebudgetFormSet(prefix='expenses')
        income_formset = IncomebudgetFormSet(prefix='incomes')
    
    template['income_formset'] = income_formset
    template['expense_formset'] = expense_formset
    template['budget'] = budget
    template['previous_budgets'] = previous_budgets
    
    return render_to_response('budget/create_budgetitems.htm',template, context_instance=RequestContext(request))

def edit_budgetitems (request, id):
#===========================================================================
# edit budget items... still broken
#===========================================================================
    template = dict()
    
    budget = Budget.objects.get(pk=id)
    
    income_items = IncomeBudgetItem.objects.filter(budget=budget)
    income_items_count = income_items.count()
    expense_items = ExpenseBudgetItem.objects.filter(budget=budget)
    expense_items_count = expense_items.count()
    
    
    ExpensebudgetFormSet = inlineformset_factory(Budget, ExpenseBudgetItem,  form=ExpenseBudgetItemForm, extra=3)
    IncomebudgetFormSet = inlineformset_factory(Budget, IncomeBudgetItem,  form=IncomeBudgetItemForm, extra=3)
    
    expense_formset = ExpensebudgetFormSet(prefix='expenses')
    income_formset = IncomebudgetFormSet(prefix='incomes')
    
    if request.method == 'POST':
        expense_formset = ExpensebudgetFormSet(request.POST, instance=budget)
        income_formset = IncomebudgetFormSet(request.POST, instance=budget)
        if expense_formset.is_valid()and income_formset.is_valid():
            count = 0
            for i in expense_items:
                i.delete()
            for i in income_items:
                i.delete()
                
            for form in expense_formset.forms:
                item = form.save(commit=False)
                if item.amount:
                    item.budget = budget
                    item.type = "EX"
                    item.save()
            for form in income_formset.forms:
                item = form.save(commit=False)
                if item.amount:
                    item.budget = budget
                    item.type = "IN"
                    item.save()
            

            
            return HttpResponseRedirect(reverse('index'))
    
    else:
        expense_formset = ExpensebudgetFormSet(instance=budget, prefix='expenses')
        income_formset = IncomebudgetFormSet(instance=budget, prefix='incomes')
    
    template['income_formset'] = income_formset
    template['expense_formset'] = expense_formset
    template['budget'] = budget
    
    return render_to_response('budget/edit_budgetitems.htm',template, context_instance=RequestContext(request))

def approved_switch(request, id):
    
    budget = Budget.objects.get(pk=id)
   
    if(budget.approved == True):
        budget.approved = False
        budget.save()
    else:
        budget.approved = True
        budget.save()

    return HttpResponseRedirect(reverse('budget_view_budgets') )

def confirm_budgetitems (request, id):
#===============================================================================
# confirm budget items
#===============================================================================
    template = dict()
    
    budget = Budget.objects.get(pk=id)
    
    budget_items_in = IncomeBudgetItem.objects.filter(budget=budget)
    budget_items_ex = ExpenseBudgetItem.objects.filter(budget=budget)
    
    in_tot = budget_items_in.aggregate(sum=Sum('amount'))
    in_tot = check(in_tot['sum'])

    ex_tot = budget_items_ex.aggregate(sum=Sum('amount'))
    ex_tot = check(ex_tot['sum'])
    
    if budget_items_in or budget_items_ex:
        template['full'] = True
     
    
    template['budget_items_in'] = budget_items_in
    template['budget_items_ex'] = budget_items_ex
    template['in_tot'] = in_tot
    template['ex_tot'] = ex_tot
    template['net'] = in_tot - ex_tot
    
    template['budget'] = budget
    
    return render_to_response('budget/confirm_budget.htm',template, context_instance=RequestContext(request))
                            
def delete_budget (request, id):
    
    template = dict()
    
    budget = get_object_or_404(Budget, pk=id)
    
    if budget.approved == False:
        budget.delete()
        delete = True
    
    template["delete"] = delete
    
    return render_to_response('budget/delete.htm',template, context_instance=RequestContext(request))



def view_budgetitems (request, id):
#===============================================================================
# view detailed view of the budget
#===============================================================================
    template = dict()
    
    budget = Budget.objects.get(pk=id)
    
    budget_items_in = IncomeBudgetItem.objects.filter(budget=budget)
    budget_items_ex = ExpenseBudgetItem.objects.filter(budget=budget)
    
    in_tot = budget_items_in.aggregate(sum=Sum('amount'))
    in_tot = check(in_tot['sum'])

    ex_tot = budget_items_ex.aggregate(sum=Sum('amount'))
    ex_tot = check(ex_tot['sum'])
    
    if budget_items_in or budget_items_ex:
        template['full'] = True
     
    
    template['budget_items_in'] = budget_items_in
    template['budget_items_ex'] = budget_items_ex
    template['in_tot'] = in_tot
    template['ex_tot'] = ex_tot
    template['net'] = in_tot - ex_tot
    
    template['budget'] = budget
    
    
    
    return render_to_response('budget/view_budgetitems.htm',template, context_instance=RequestContext(request))
                            