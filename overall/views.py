#python functionality
import datetime
from pygooglechart import SimpleLineChart, Axis, PieChart3D, PieChart2D, StackedHorizontalBarChart, StackedVerticalBarChart, BarChart


from decimal import *
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

def current_term():
    
    today = datetime.date.today()
    
    if today.month < 5:
        term = 'W'
    elif today.month < 9:
        term =  'S'
    else:
        term = 'F'

    return term

def find_next_term(term, year):
    
    if term == 'W':
        next_term = 'S'
        next_year = year
    elif term == 'S':
        next_term = 'F'
        next_year = year
    elif term == 'F':
        next_term = 'W'
        next_year = year + 1
    return next_term, next_year

def find_prev_term(term, year):
    
    if term == 'W':
        prev_term = 'F'
        prev_year = year - 1
    elif term == 'S':
        prev_term = 'W'
        prev_year = year
    elif term == 'F':
        prev_term = 'S'
        prev_year = year
    return prev_term, prev_year

def create_category_charts(expenditure_category, income_category):
    #===========================================================================
    # chart stuff 
    #===========================================================================
    category = []
    categoryamount = []
    incomecategorylist = income_category
    for c in incomecategorylist:
        categoryamount.append(int(c['sum']))
#        percent = c['totalcategory'] / income_total['total'] * 100
        category.append(c['income_category__name'])                              
#        category.append('%s (%d%%)' % (c['category__name'], percent))
    
    incomecategoryBreakdownChart = PieChart3D(375, 125)
    incomecategoryBreakdownChart.add_data(categoryamount)

    incomecategoryBreakdownChart.set_colours(['045FB4', '2E9AFE', '81BEF7', 'CEE3F6' ])
    incomecategoryBreakdownChart.set_pie_labels(category)
    incomeChart = incomecategoryBreakdownChart.get_url()
    
    category = []
    categoryamount = []
    expenditurecategorylist = expenditure_category
    for c in expenditurecategorylist:
        categoryamount.append(int(c['sum']))                                
        category.append(c['expenditure_category__name'])
    #categorys = sorted(categorys)
    
    expenditurecategoryBreakdownChart = PieChart3D(375, 125)
    expenditurecategoryBreakdownChart.add_data(categoryamount)
    
    expenditurecategoryBreakdownChart.set_colours(['045FB4', '2E9AFE', '81BEF7', 'CEE3F6' ])
    expenditurecategoryBreakdownChart.set_pie_labels(category)
    expenditureChart = expenditurecategoryBreakdownChart.get_url()
    
    return incomeChart, expenditureChart


def overview_page(request, term=None, year=None):
    template = dict()
    
#    users-specific information
    user_trans = Transaction.objects.filter(creator=request.user)
    user_budgets = Budget.objects.filter(creator=request.user)
    template['user_trans'] = user_trans
    template['user_budgets'] = user_budgets
    
    categories_in = IncomeCategory.objects.filter(isactive=True)
    categories_ex = ExpenditureCategory.objects.filter(isactive=True)
    
#    filter for term
    if not year:
        year = datetime.date.today().year
    if not term:
        term = current_term()
    
    next_term = term
    next_year = year
    
    year = int(year)
    term = str(term)
    template['year'] = year
    template['term'] = term
    
#    find previous and next terms
    next_term, next_year = find_next_term(term, year)
    template['next_term'] = next_term
    template['next_year'] = next_year
    
    prev_term, prev_year = find_prev_term(term, int(year))
    template['prev_term'] = prev_term
    template['prev_year'] = prev_year
    
                  
    overall_budget_in_items = IncomeBudgetItem.objects.filter(budget__start_date__year=year, budget__term=term, budget__approved=True)
    overall_budget_ex_items = ExpenseBudgetItem.objects.filter(budget__start_date__year=year, budget__term=term, budget__approved=True)
    overall_actual_in_items = Income.objects.filter(year=year, term=term, approved=True)
    overall_actual_ex_items = Expenditure.objects.filter(year=year, term=term, approved=True)    
    
#    overall budgeted - by category
    overall_budget_in_cat = overall_budget_in_items.values('income_category__name').annotate(sum=Sum('amount'))
    template['overall_budget_in_cat'] = overall_budget_in_cat
    sum_budget_in = overall_budget_in_items.aggregate(sum=Sum('amount'))
    template['sum_budget_in'] = check(sum_budget_in['sum'])
    

    overall_budget_ex_cat = overall_budget_ex_items.values('expenditure_category__name').annotate(sum=Sum('amount'))
    template['overall_budget_ex_cat'] = overall_budget_ex_cat
    sum_budget_ex = overall_budget_ex_items.aggregate(sum=Sum('amount'))
    template['sum_budget_ex'] = check(sum_budget_ex['sum'])
    
    template['sum_budget_net'] = template['sum_budget_in'] - template['sum_budget_ex']
    
    #    make category breakdown charts
    try:
        incomeChart, expenditureChart = create_category_charts(overall_budget_ex_cat, overall_budget_in_cat)
    except:
        incomeChart = None
        expenditureChart = None
    
    template["income_chart"] = incomeChart
    template["expenditure_chart"] = expenditureChart
    
#    overall actual - by cateogry
    overall_actual_in_cat = overall_actual_in_items.values('income_category__name').annotate(sum=Sum('amount'))
    template['overall_actual_in_cat'] = overall_actual_in_cat
    sum_actual_in = overall_actual_in_items.aggregate(sum=Sum('amount'))
    template['sum_actual_in'] = check(sum_actual_in['sum'])
    

    overall_actual_ex_cat = overall_actual_ex_items.values('expenditure_category__name').annotate(sum=Sum('amount'))
    template['overall_actual_ex_cat'] = overall_actual_ex_cat
    sum_actual_ex = overall_actual_ex_items.aggregate(sum=Sum('amount'))
    template['sum_actual_ex'] = check(sum_actual_ex['sum'])
    
#    make tables to display budgeted and actual - by category
    budget_actual_in_cat_table = []
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
        budget_actual_in_cat_table.append(line)
        
    template['budget_actual_in_cat_table'] = budget_actual_in_cat_table
    
    budget_actual_ex_cat_table = []
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
        budget_actual_ex_cat_table.append(line)
        
    template['budget_actual_ex_cat_table'] = budget_actual_ex_cat_table
    
    
#    overall budgeted - by position
    overall_budget_in_pos = overall_budget_in_items.values('budget__position__name').annotate(sum=Sum('amount'))
    template['overall_budget_in_pos'] = overall_budget_in_pos
    
    overall_budget_ex_pos = overall_budget_ex_items.values('budget__position__name').annotate(sum=Sum('amount'))
    template['overall_budget_ex_pos'] = overall_budget_ex_pos

#    make tables to display budgeted and actual - by position
    positions = Position.objects.filter(isactive=True)
    budget_actual_pos_table = []
    for p in positions:
        line = dict()
        line['position'] = p.name
        line['budgeted_in'] = 0
        line['budgeted_ex'] = 0
        line['net'] = 0.00
        for b in overall_budget_in_pos:
            if p.name == b['budget__position__name']:
                line['budgeted_in'] = b['sum']
        for a in overall_budget_ex_pos:
            if p.name == a['budget__position__name']:
                line['budgeted_ex'] = a['sum']
        line['net'] = line['budgeted_in'] - line['budgeted_ex']
        budget_actual_pos_table.append(line)
        
    template['budget_actual_pos_table'] = budget_actual_pos_table
    
    
    return render_to_response('overall/index.htm',template, context_instance=RequestContext(request))
    
     
def logout_view(request):
    logout(request) 
    
    return HttpResponseRedirect(reverse('overview_page'))
    
    
    
    
    