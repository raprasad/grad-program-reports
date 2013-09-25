from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from graduate_students.utils.view_util import get_basic_view_dict, get_not_logged_in_page
from dissertation.models import *
from dac_meetings.forms import DacForm
from advisory_committee.models import Advisor as ThesisAdvisor
from dac_meetings.dac_xls_maker import make_dac_report
from datetime import datetime
import xlwt

def get_dac_meetings(dac_kwarg_lookup):
    if dac_kwarg_lookup is None:
        return None
    
    # Get a list of student ids
    dac_student_ids = RequiredMeeting.objects.values_list('student__id', flat=True\
                             ).filter(**dac_kwarg_lookup)
    
    # Use this list to make a dict of { student.id : [advisor 1, advisor 2] }
    advisor_lookup = {}                         
    for advisor in ThesisAdvisor.objects.select_related('faculty_member', 'faculty_member__department', 'student'\
                                    ).filter(student__id__in=dac_student_ids, active=True):
        advisor_lookup.setdefault(advisor.student.id, []).append(advisor.faculty_member)
        
    # Retrieve the DAC meetings
    dac_meetings = RequiredMeeting.objects.select_related('student', 'student__status', 'status'\
                         ).filter(**dac_kwarg_lookup\
                         ).order_by('meeting_type', 'student__last_name')
    
    # For dissertations, add the has paper
    
    
    # Add the "current_advisors" attribute to each DAC
    fmt_dac_meetings = []
    for dac in dac_meetings:
        dac.current_advisors = advisor_lookup.get(dac.student.id)
        fmt_dac_meetings.append(dac)
    return fmt_dac_meetings
    
def view_dac_meeting_report(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponseRedirect(get_not_logged_in_page())
    
    lu = { 'DAC_MEETING_REPORT_PAGE' : True \
                  , 'page_title' : 'DAC Meeting Report'\
                  , 'RM_STATUS_SCHEDULED' : RM_STATUS_SCHEDULED
                  , 'RM_FAIL_STATUSES' : RM_FAIL_STATUSES
            }
    dac_kwargs = {}
    
    dac_meetings = None
    num_dac_meetings = 0
    if request.method=='GET' and request.GET.has_key('start_date'):        
         dac_form = DacForm(request.GET)
         if dac_form.is_valid():
             dac_kwargs.update(dac_form.get_dac_kwargs())
             dac_meetings =  get_dac_meetings(dac_kwargs)
             num_dac_meetings = len(dac_meetings)
         else:
             print 'NOT valid!'
             lu.update({ 'ERR_form_not_valid' : True })
    else: 
         dac_form = DacForm()

        
    lu.update({ 'dac_meetings' :  dac_meetings\
            , 'num_dac_meetings' : num_dac_meetings\
            , 'dac_form' : dac_form\
            , 'QUERY_STRING' : request.META['QUERY_STRING'] 
        })
    
    return render_to_response('dac_meetings/dac_meetings.html', lu, context_instance=RequestContext(request))
    
    
    #return HttpResponse('view_dac_meeting_report')
    
    
    
def view_dac_meeting_report_spreadsheet(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponseRedirect(get_not_logged_in_page())
    
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponseRedirect(get_not_logged_in_page())

    dac_kwargs = {}

    if request.method=='GET' and request.GET.has_key('start_date'):        
         dac_form = DacForm(request.GET)
         if dac_form.is_valid():
             dac_kwargs.update(dac_form.get_dac_kwargs())

    dac_meetings = get_dac_meetings(dac_kwargs)

    
    book = xlwt.Workbook(encoding="utf-8")
    # With a workbook object made we can now add some sheets.
    sheet1 = book.add_sheet(slugify('DAC'))

    date_obj = datetime.now()

    sheet1 = make_dac_report(sheet1, dac_meetings)

    # create response object
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=dac_%s.xls' % ( date_obj.strftime('%m%d-%I-%M%p-%S').lower())

    # send .xls spreadsheet to response stream
    book.save(response)
    return response