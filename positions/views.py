from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from positions.models import Position, PositionForm




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

def view_positions(request, criteria):
    template = dict()
    
    if criteria == 'all':
        positions = Position.objects.all()
    elif criteria == 'active':
        positions = Position.objects.filter(isactive=True)
    elif criteria == 'inactive':
        positions = Position.objects.filter(isactive=False)
    
    template['positions'] = positions
    template['criteria'] = criteria
    
    return render_to_response('positions/view_positions.htm',template, context_instance=RequestContext(request))

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

    