#python functionality
import datetime

#django functionality
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, Count, Sum
from django.contrib.auth import logout

from positions.models import Position
from categories.models import Category, IncomeCategory, ExpenditureCategory
from transactions.models import Transaction, Income, Expenditure
from budget.models import Budget, BudgetItem, IncomeBudgetItem, ExpenseBudgetItem


def check(check):
#===============================================================================
# helper function to check for null values
#===============================================================================
    if not check:
        check = 0
    return check

def is_admin(user):
    if user:
        return user.groups.filter(name='admin').count() != 0
    return False

def is_vpf(user):
    if user:
        return user.groups.filter(name='vpf').count() != 0
    return False

def overview_page(request):
    template = dict()
    
#    users-specific information
    user_trans = Transaction.objects.filter(creator=request.user)
    user_budgets = Budget.objects.filter(creator=request.user)
    template['user_trans'] = user_trans
    template['user_budgets'] = user_budgets
    
    categories_in = IncomeCategory.objects.filter(isactive=True)
    categories_ex = ExpenditureCategory.objects.filter(isactive=True)
    
#    overall budgeted
    overall_budget_in_items = IncomeBudgetItem.objects.all()
    overall_budget_in_cat = overall_budget_in_items.values('income_category__name').annotate(sum=Sum('amount'))
    template['overall_budget_in_cat'] = overall_budget_in_cat
    sum_budget_in = overall_budget_in_items.aggregate(sum=Sum('amount'))
    template['sum_budget_in'] = check(sum_budget_in['sum'])
    
    overall_budget_ex_items = ExpenseBudgetItem.objects.all()
    overall_budget_ex_cat = overall_budget_ex_items.values('expenditure_category__name').annotate(sum=Sum('amount'))
    template['overall_budget_ex_cat'] = overall_budget_ex_cat
    sum_budget_ex = overall_budget_ex_items.aggregate(sum=Sum('amount'))
    template['sum_budget_ex'] = check(sum_budget_ex['sum'])
    
#    overall actual
    overall_actual_in_items = Income.objects.all()
    overall_actual_in_cat = overall_actual_in_items.values('income_category__name').annotate(sum=Sum('amount'))
    template['overall_actual_in_cat'] = overall_actual_in_cat
    sum_actual_in = overall_actual_in_items.aggregate(sum=Sum('amount'))
    template['sum_actual_in'] = check(sum_actual_in['sum'])
    
    overall_actual_ex_items = Expenditure.objects.all()
    overall_actual_ex_cat = overall_actual_ex_items.values('expenditure_category__name').annotate(sum=Sum('amount'))
    template['overall_actual_ex_cat'] = overall_actual_ex_cat
    sum_actual_ex = overall_actual_ex_items.aggregate(sum=Sum('amount'))
    template['sum_actual_ex'] = check(sum_actual_ex['sum'])
    
#    make tables to display budgeted and actual
    budget_actual_in_table = []
    for c in categories_in:
        line = dict()
        line['category'] = c.name
        line['budgeted'] = 0.00
        line['actual'] = 0.00
        for b in overall_budget_in_cat:
            if c.name == b['income_category__name']:
                line['budgeted'] = b['sum']
        for a in overall_actual_in_cat:
            if c.name == a['income_category__name']:
                line['actual'] = a['sum']
        budget_actual_in_table.append(line)
        
    template['budget_actual_in_table'] = budget_actual_in_table
    
    budget_actual_ex_table = []
    for c in categories_ex:
        line = dict()
        line['category'] = c.name
        line['budgeted'] = 0.00
        line['actual'] = 0.00
        for b in overall_budget_ex_cat:
            if c.name == b['expenditure_category__name']:
                line['budgeted'] = b['sum']
        for a in overall_actual_ex_cat:
            if c.name == a['expenditure_category__name']:
                line['actual'] = a['sum']
        budget_actual_ex_table.append(line)
        
    template['budget_actual_ex_table'] = budget_actual_ex_table
    
    
    return render_to_response('overall/index.htm',template, context_instance=RequestContext(request))
    
     
def logout_view(request):
    logout(request) 
    
    return HttpResponseRedirect(reverse('overview_page'))
    
    
    
    
    