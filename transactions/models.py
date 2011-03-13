#import from django
from django.db import models
from django.forms import ModelForm  #used for creating automatic forms
from django import forms
from django.core.exceptions import ObjectDoesNotExist

#import python utility
import datetime

#import from 461designproject
from categories.models import IncomeCategory, ExpenditureCategory

from budget.models import Budget
from positions.models import Position

#predefined choices
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


#start model defintion

class Transaction(models.Model):  
    date = models.DateField('Date (YYYY-MM-DD)', null=True, blank=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length = 100)
    approved = models.BooleanField(default=False)
    cheque_ready = models.BooleanField(default=False)
    term = models.CharField(max_length = 1, choices=TERM_CHOICES)
    year = models.IntegerField('Year')

#    automatic fields
    date_submitted = models.DateField('Enter Date', auto_now_add=True)
    type = models.CharField(max_length = 2, choices=TYPE_CHOICES) #income or expenditure
 
#    linked objects - foreign keys go here
    position = models.ForeignKey(Position)
    budget = models.ForeignKey(Budget)

    def __unicode__(self):
        return u'%s %s' %(self.date, self.amount)
    
class Income(Transaction):
    income_category = models.ForeignKey(IncomeCategory, null=True)
    def __unicode__(self):
        return u'%s %s' %(self.date, self.amount)
    

    
class Expenditure(Transaction):
    expenditure_category = models.ForeignKey(ExpenditureCategory, null=True)
    receipt_img = models.FileField('Receipt Image', upload_to = 'receipt_images', null=True, blank=True)
    hst = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    #   New fields added by Katrina
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
        
    def __unicode__(self):
        return u'%s %s' %(self.payee, self.amount)



#forms on the website
class IncomeForm(ModelForm):
    
    class Meta:
        model = Income
        exclude = ('approved', 'cheque_ready', 'budget', 'type')
        
    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['income_category'].queryset = IncomeCategory.objects.filter(isactive=True)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        term = cleaned_data['term']
        year = cleaned_data['year']
        position = cleaned_data['position']
        if term and year and position:
            try:
                budget = Budget.objects.get(term=term, year=year, position=position)
            except ObjectDoesNotExist:
                raise forms.ValidationError("There is no existing budget for specified term, year and position. Please check again.")

        return cleaned_data

class ExpenditureForm(ModelForm):
    
    class Meta:
        model = Expenditure
        exclude = ('approved', 'cheque_ready', 'budget', 'type')
    
    def __init__(self, *args, **kwargs):
        super(ExpenditureForm, self).__init__(*args, **kwargs)
        self.fields['expenditure_category'].queryset = ExpenditureCategory.objects.filter(isactive=True)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        term = cleaned_data['term']
        year = cleaned_data['year']
        position = cleaned_data['position']
        if term and year and position:
            try:
                budget = Budget.objects.get(term=term, year=year, position=position)
            except ObjectDoesNotExist:
                raise forms.ValidationError("There is no existing budget for specified term, year and position. Please check again.")

        return cleaned_data
    
    