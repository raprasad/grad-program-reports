from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from graduate_students.utils.view_util import get_basic_view_dict, get_not_logged_in_page
from graduate_students.faculty.models import FacultyMember, FacultyStatus
from graduate_students.faculty_assistant.models import FacultyAssistant
from graduate_students.building.models import Building
from django.template.defaultfilters import slugify

from faculty_info.faculty_contaxt_xls_maker import make_faculty_contact_report
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
    
    lu = get_basic_view_dict(request)
    
    lu.update( { 'FACULTY_INFO_PAGE' : True \
            , 'FACULTY_CONTACT_INFO' : True\
            , 'page_title' : 'Faculty Contacts'\
         })
    
    
    faculty_member_kwargs = {}

    faculty_members = None
    num_faculty_members = 0
    no_faculty_members_found = False
    
    if request.method=='GET' and request.GET.has_key('faculty_status'):        
        contact_form = ContactForm(request.GET)
        if contact_form.is_valid():
            faculty_member_kwargs.update(contact_form.get_faculty_info_kwargs())
            faculty_members = get_faculty_members(faculty_member_kwargs)
            num_faculty_members = len(faculty_members)
            if num_faculty_members == 0:
                no_faculty_members_found = True
        else:
            print 'NOT valid!'
            lu.update({ 'ERR_form_not_valid' : True })
    else: 
        contact_form = ContactForm()
   
       
    lu.update({ 'faculty_members' :  faculty_members\
            , 'num_faculty_members' : num_faculty_members\
            , 'no_faculty_members_found' : no_faculty_members_found
            , 'contact_form' : contact_form\
            , 'QUERY_STRING' : request.META['QUERY_STRING'] 
        })
    
    return render_to_response('faculty_info/contact_info.html', lu, context_instance=RequestContext(request))
    
    
    #return HttpResponse('view_dac_meeting_report')
    
   
    
def view_faculty_contacts_spreadsheet(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponseRedirect(get_not_logged_in_page())
    
    if not (request.user.is_authenticated and request.user.is_staff):
        return HttpResponseRedirect(get_not_logged_in_page())

    faculty_member_kwargs = {}

    if request.method=='GET' and request.GET.has_key('faculty_status'):        
        contact_form = ContactForm(request.GET)
        if contact_form.is_valid():
             faculty_member_kwargs.update(contact_form.get_faculty_info_kwargs())
                

    faculty_members = get_faculty_members(faculty_member_kwargs)

    
    book = xlwt.Workbook(encoding="utf-8")
    # With a workbook object made we can now add some sheets.
    sheet1 = book.add_sheet(slugify('Faculty Contacts'))

    date_obj = datetime.now()

    sheet1 = make_faculty_contact_report(sheet1, faculty_members)

    # create response object
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=faculty_contacts_%s.xls' % ( date_obj.strftime('%m%d-%I-%M%p-%S').lower())

    # send .xls spreadsheet to response stream
    book.save(response)
    return response
