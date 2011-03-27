from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm  #used for creating forms at bottom of page
from django.forms import forms
from django import forms
from django.contrib.auth.models import User

# import from other apps
from positions.models import Position
from categories.models import IncomeCategory, ExpenditureCategory

TYPE_CHOICES = (
    ('EX','Expenditure'),
    ('IN', 'Income')
)

STREAM_CHOICES = (
    ('A','A Stream'),
    ('B', 'B Stream')
)

TERM_CHOICES = (
    ('S','Spring'),
    ('F', 'Fall'),
    ('W', 'Winter')
)

class Budget(models.Model):
#    budget name can be removed (MFP meeting)

    term = models.CharField(max_length = 1, choices=TERM_CHOICES)
    year = models.IntegerField('Year')
    stream = models.CharField(max_length = 1, choices=STREAM_CHOICES)
    approved = models.BooleanField(default=False)
    
#    automatically created
    created = models.DateField('Date Created', auto_now_add=True)
    start_date = models.DateField('Start Date (YYYY-MM-DD)')
    end_date = models.DateField('End Date (YYYY-MM-DD)')
    
#    linked objects
    position = models.ForeignKey(Position)
    creator = models.ForeignKey(User, related_name="budget_creator")
#    edited_by = models.ForeignKey(User, related_name="budget_edited")
    
    def __unicode__(self):
        return u'%s %s-%s' %(self.name, self.term, self.year)

class BudgetItem(models.Model):

    type = models.CharField(max_length = 2, choices=TYPE_CHOICES)
    description = models.CharField('Description', max_length = 100)

#    new entries for form added by Katrina
    amount_per_item = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    num_items = models.DecimalField(max_digits=10, decimal_places=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
#    linked objects
    budget = models.ForeignKey(Budget)
    
    
class IncomeBudgetItem(BudgetItem):
    
    income_category = models.ForeignKey(IncomeCategory)
    
    def __unicode__(self):
        return u'%s %s-%s' %(self.description, self.amount, self.amount_per_item)
    
class ExpenseBudgetItem(BudgetItem):
    
    expenditure_category = models.ForeignKey(ExpenditureCategory)

    def __unicode__(self):
        return u'%s %s-%s' %(self.description, self.amount, self.amount_per_item)
    
class IncomeBudgetItemForm(ModelForm):
    class Meta:
        model = IncomeBudgetItem
        exclude = ('budget', 'type')
        fields = ['description', 'amount_per_item', 'num_items', 'amount', 'income_category']
    
    def __init__(self, *args, **kwargs):
        super(IncomeBudgetItemForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = IncomeBudgetItem
        exclude = ('budget', 'type', 'budgetitem_ptr')

class ExpenseBudgetItemForm(ModelForm):
    class Meta:
        model = ExpenseBudgetItem
        exclude = ('budget', 'type')
        fields = ['description', 'amount_per_item', 'num_items', 'amount', 'expenditure_category']
    
    def clean_amount(self):
        cleaned_data = self.cleaned_data
        amount_per_item = cleaned_data.get('amount_per_item')
        num_items = cleaned_data.get('num_items')
        amount = cleaned_data.get('amount')
        
        if amount_per_item*num_items != amount:
            raise forms.ValidationError,"Amount must equal $/item * number of items."
        return amount
    
    def __init__(self, *args, **kwargs):
        super(ExpenseBudgetItemForm, self).__init__(*args, **kwargs)
        self.fields['expenditure_category'].queryset = ExpenditureCategory.objects.filter(isactive=True)



class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        exclude = ('creator', 'edited_by', 'start_date', 'end_date', 'approved')
    
    def __init__(self, *args, **kwargs):
        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['position'].queryset = Position.objects.filter(isactive=True)