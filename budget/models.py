from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm  #used for creating forms at bottom of page
from django.forms import forms
from django import forms

# import from other apps
from positions.models import Position
from transactions.models import IncomeCategory, ExpenditureCategory

TYPE_CHOICES = (
    ('EX','Expenditure'),
    ('IN', 'Income')
)

STREAM_CHOICES = (
    ('A','A Stream'),
    ('B', 'B Stream')
)

class Budget(models.Model):
    name = models.CharField('Budget Name', max_length = 30)
    start_date = models.DateField('Start Date (YYYY-MM-DD)')
    end_date = models.DateField('End Date (YYYY-MM-DD)')
    stream = models.CharField(max_length = 1, choices=STREAM_CHOICES)
    
#    automatically created
    created = models.DateField('Date Created', auto_now_add=True)
    
#    linked objects
    position = models.ForeignKey(Position)
#    creator = models.ForeignKey(User, related_name="budget_created")
#    edited_by = models.ForeignKey(User, related_name="budget_edited")
    
    def __unicode__(self):
        return u'%s %s-%s' %(self.name, self.start_date, self.end_date)

class BudgetItem(models.Model):

    type = models.CharField(max_length = 2, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
#    linked objects
    budget = models.ForeignKey(Budget)
    income_category = models.ForeignKey(IncomeCategory)
    expenditure_category = models.ForeignKey(ExpenditureCategory)
    
class BudgetItemForm(ModelForm):
    class Meta:
        model = BudgetItem
        exclude = ('budget')

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        exclude = ('creator', 'edited_by')