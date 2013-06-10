from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from dissertation.models import *

def view_dac_meeting_report(request):
    
    
    lu = { 'DAC_MEETING_REPORT_PAGE' : True \
            , 'page_title' : 'DAC Meeting Report'
            , 'dac_meetings' :  RequiredMeeting.objects.select_related('student').all().order_by('meeting_type')[:10]
        }
    
    return render_to_response('dac_meetings.html', lu, context_instance=RequestContext(request))
    
    
    #return HttpResponse('view_dac_meeting_report')
    
    
    
def view_dac_meeting_report_spreadsheet(request):
    return HttpResponse('view_dac_meeting_report_spreadsheet')