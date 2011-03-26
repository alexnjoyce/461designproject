from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

import csv

from positions.models import Position, PositionForm, UploadDataForm
from settings import MEDIA_ROOT



@login_required
def create_position(request):
    template = dict()
    
#   if the form has been submitted
    if request.method == 'POST': 
        form = PositionForm(request.POST)

        #validate fields
        if form.is_valid(): # check if fields validated
            cleaned_data = form.cleaned_data
            form.save()
            return HttpResponseRedirect(reverse('position_view_positions', kwargs={'criteria': "all"}))

            
    #else blank form   
    else:
        form = PositionForm()

    template['form'] = form
    
    #tells the view which template to use, and to pass the template dictionary
    return render_to_response('positions/create_positions.htm',template, context_instance=RequestContext(request))

@login_required
def view_positions(request, criteria):
    template = dict()
    
    criteria_list = []
    criteria_list.append('active')
    criteria_list.append('inactive')
    
    template['criteria_list'] = criteria_list
    
    if criteria == 'all':
        positions = Position.objects.all()
    elif criteria == 'active':
        positions = Position.objects.filter(isactive=True)
    elif criteria == 'inactive':
        positions = Position.objects.filter(isactive=False)
    
    template['positions'] = positions
    template['criteria'] = criteria
    
    return render_to_response('positions/view_positions.htm',template, context_instance=RequestContext(request))

@login_required
def isactive_switch(request, state, id):
    
    position = Position.objects.get(pk=id)
   
    if(position.isactive == True):
        position.isactive = False
        position.save()
    else:
        position.isactive = True
        position.save()
    
    criteria = state

    return HttpResponseRedirect(reverse('position_view_positions', kwargs={'criteria': criteria}) )

@login_required
def upload_data(request):
    
    template = dict()
    
    if request.method == 'POST':
        
        form = UploadDataForm(request.POST, request.FILES)
        if form.is_valid():             
            
            directory = MEDIA_ROOT + "/test_data/" + request.FILES["file"].name
            
            reader = csv.reader(open(directory))
            
            for r in reader:
                position = Position()
                position.name = r[0]
                position.isactive = True
                position.save()
            return HttpResponseRedirect(reverse('position_view_positions', kwargs={'criteria': "all"}))

            
        
    else:
        form = UploadDataForm()
    
    template['form'] = form
    
    return render_to_response('positions/upload_positions.htm',template, context_instance=RequestContext(request))    
    

    