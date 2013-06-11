from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q

from graduate_students.utils.view_util import get_basic_view_dict, get_not_logged_in_page
from dissertation.models import *
from dac_meetings.forms import DacForm

def view_dac_meeting_report(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponseRedirect(get_not_logged_in_page())
    
    lu = { 'DAC_MEETING_REPORT_PAGE' : True \
                  , 'page_title' : 'DAC Meeting Report'\
            }
    dac_kwargs = {}
    
    if request.method=='POST':        
         dac_form = DacForm(request.POST)
         if dac_form.is_valid():
             dac_kwargs.update(dac_form.get_dac_kwargs())
             #return HttpResponse('valid')
             #tweet_form.send_tweet()
             #return HttpResponseRedirect(reverse('view_tweet_success', args=()))
         else:
             print 'NOT valid!'
             lu.update({ 'ERR_form_not_valid' : True })
    else: 
         dac_form = DacForm()

    dac_meetings = RequiredMeeting.objects.select_related('student'\
                     ).filter(**dac_kwargs).order_by('meeting_type')[:10]
    

    lu.update({ 'dac_meetings' :  dac_meetings
            , 'dac_form' : dac_form
        })
    
    return render_to_response('dac_meetings.html', lu, context_instance=RequestContext(request))
    
    
    #return HttpResponse('view_dac_meeting_report')
    
    
    
def view_dac_meeting_report_spreadsheet(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponseRedirect(get_not_logged_in_page())
    
    return HttpResponse('view_dac_meeting_report_spreadsheet')