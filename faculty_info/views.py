from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from graduate_students.utils.view_util import get_basic_view_dict, get_not_logged_in_page
from graduate_students.faculty.models import FacultyMember, FacultyStatus
from graduate_students.faculty_assistant.models import FacultyAssistant
from graduate_students.building.models import Building

from faculty_info.forms_contact import ContactForm
#from dac_meetings.dac_xls_maker import make_dac_report
from datetime import datetime
import xlwt

def get_faculty_members(faculty_member_kwargs):
    
    return FacultyMember.objects.select_related('faculty_assistant'\
                        , 'faculty_assistant__building'\
                        , 'department'\
                        , 'building'\
                    ).filter(**faculty_member_kwargs\
                    ).order_by('department', 'last_name', 'first_name')


def view_faculty_contacts(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponseRedirect(get_not_logged_in_page())
    
    lu = { 'FACULTY_INFO_PAGE' : True \
            , 'FACULTY_CONTACT_INFO' : True\
            , 'page_title' : 'Faculty Contacts (active faculty)'\
         }
    
    
    faculty_member_kwargs = {}

    faculty_members = None
    num_faculty_members = 0
    
    if request.method=='GET' and request.GET.has_key('faculty_status'):        
        contact_form = ContactForm(request.GET)
        if contact_form.is_valid():
            faculty_member_kwargs.update(contact_form.get_faculty_info_kwargs())
            faculty_members = get_faculty_members(faculty_member_kwargs)
            num_faculty_members = len(faculty_members)
        else:
            print 'NOT valid!'
            lu.update({ 'ERR_form_not_valid' : True })
    else: 
        contact_form = ContactForm()
    """        
    faculty_members = FacultyMember.objects.select_related('faculty_assistant'\
                            , 'faculty_assistant__building'\
                            , 'department'\
                            , 'building'\
                        ).filter(is_active=True\
                            #, last_name='Denic'\
                        ).order_by('department', 'last_name', 'first_name')
    """
       
    lu.update({ 'faculty_members' :  faculty_members\
            , 'num_faculty_members' : num_faculty_members\
            , 'contact_form' : contact_form\
            , 'QUERY_STRING' : request.META['QUERY_STRING'] 
        })
    
    return render_to_response('faculty_info/contact_info.html', lu, context_instance=RequestContext(request))
    
    
    #return HttpResponse('view_dac_meeting_report')
    
"""    
    
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
"""