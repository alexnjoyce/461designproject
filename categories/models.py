#import from django
from django.db import models
from django.forms import ModelForm  #used for creating forms at bottom of page
from django.forms import forms
from django import forms
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField('Category Name', max_length = 50)
    isactive = models.BooleanField()
    
#    automatically created
    created = models.DateField('Date Created', auto_now_add=True)
    
#    linked objects
#    created_by = models.ForeignKey(User)
#    edited_by = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s' %(self.name)
    
class IncomeCategory(Category):

    def __unicode__(self):
        return u'%s' %(self.name)
    
class ExpenditureCategory(Category):

    def __unicode__(self):
        return u'%s' %(self.name) 
    
#forms on the website
class IncomeCategoryForm(ModelForm):
    
    class Meta:
        model = IncomeCategory
        
class ExpenditureCategoryForm(ModelForm):
    
    class Meta:
        model = ExpenditureCategory
        
#===============================================================================
# form for uploading test data
#===============================================================================

class UploadDataForm(forms.Form):
    file  = forms.FileField()