from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory

from positions.models import Position
from budget.models import Budget, BudgetItem, BudgetItemForm, BudgetForm

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
            form.save()
            return HttpResponseRedirect(reverse('index'))
            
    #else blank form   
    else:
        form = BudgetForm()

    template['form'] = form
    
    #tells the view which template to use, and to pass the template dictionary
    return render_to_response('budget/create_budget.htm',template, context_instance=RequestContext(request))

def view_budgets(request):
    template = dict()
    
    budgets = Budget.objects.all()
    
    template['budgets'] = budgets
    
    return render_to_response('budget/view_budget.htm',template, context_instance=RequestContext(request))

def create_budgetitems (request, id):
    template = dict()
    
    budget = Budget.objects.get(pk=id)
    
    budgetFormSet = formset_factory(BudgetItemForm, extra=5)
    
    if request.method == 'POST':
        formset = budgetFormSet(request.POST)
        if formset.is_valid():
            count = 0
            for form in formset.forms:
                item = form.save(commit=False)
                item.budget = budget
                item.save()
            
            return HttpResponseRedirect(reverse('index'))
    
    else:
        formset = budgetFormSet()
    
    template['formset'] = formset
    template['budget'] = budget
    
    return render_to_response('budget/create_budgetitems.htm',template, context_instance=RequestContext(request))
                                 