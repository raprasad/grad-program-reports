import xlwt
from xlwt import easyxf, Formula
from graduate_students.utils.xls_styles import *

from django.core.urlresolvers import reverse
from django.conf import settings
#from django.contrib.sites.models import Site

    
def fmt_faculty_member(faculty_member):
    if faculty_member is None:
        return ''
    
    if faculty_member.second_department:
        fm_text = '%s (%s / %s)' % (faculty_member\
                , faculty_member.department.abbreviation\
                , faculty_member.second_department.abbreviation\
                
                )
    else:
        fm_text = '%s (%s)' % (faculty_member, faculty_member.department.abbreviation)

    return fm_text

        
def get_student_link(gs):
    #link = 'HYPERLINK("http://stackoverflow.com/"; "SO")'
    #    sheet.write(0, 0, Formula(link))
    current_site = Site.objects.get(id=settings.SITE_ID)
    
    lnk =  reverse('view_student_profile', kwargs={'student_hash': gs.id_hash })
    lnk2 = 'http://%s%s' % ( current_site.domain, lnk)
    return 'HYPERLINK("%s";"%s")' % (lnk2, gs.last_name)
    
    #return '<a href="%s">%s</a>' % (lnk, fm)

def make_dac_report(sheet1, dac_meetings, **kwargs):
    """Spreadsheet for MCB Core admin use"""
    if sheet1 is None:
        return None
    if dac_meetings is None:
        return sheet
                  

    #   (header label, attribute, width)
    column_attributes = [ 
     
     ('Last Name', 'student', 15)
    ,('First Name', '--skip--', 15)
    ,('MCB Year', '--skip--', 10)
    ,('Student Status', '--skip--', 20)

    ,('Advisor', 'advisors', 25)

    , ('Meeting Type', 'meeting_type', 20)
    ,('Meeting Status', 'status', 20)
    ,('Date', 'date', 10)
    
    ,('Nominated for Prize', 'nominated_for_prize', 10)
    ]
    
 
    #----------------------------
    # Add the header row and set column widths
    #----------------------------
    char_multiplier = 256
    excel_row_num = 0
    for col_idx, (col_name, attr_name, col_width) in enumerate(column_attributes):
        sheet1.write(excel_row_num, col_idx, col_name, style_header)
        sheet1.col(col_idx).width = col_width * char_multiplier  

    #   Add data to the spreadsheet
    #
    for dac in dac_meetings:
        excel_row_num +=1

        for col_idx, (col_name, attr, col_width) in enumerate(column_attributes):
            if attr == '--skip--':
                continue
                
            if attr == 'student':
                sheet1.write(excel_row_num, col_idx,  dac.student.last_name, style_info_cell_wrap_on)  
                sheet1.write(excel_row_num, col_idx+1,  dac.student.first_name, style_info_cell_wrap_on)  
                sheet1.write(excel_row_num, col_idx+2, 'G%s' % dac.student.mcb_year, style_info_cell_wrap_on)  
                sheet1.write(excel_row_num, col_idx+3,  '%s' % dac.student.status, style_info_cell_wrap_on)  
                
            elif attr == 'date':
                sheet1.write(excel_row_num, col_idx,  dac.date.strftime('%m/%d/%Y'), style_info_cell_wrap_on)  
            elif attr == 'nominated_for_prize':
            
                if dac.nominated_for_prize:
                    val = 'Yes'
                else:
                    val = 'No'
                sheet1.write(excel_row_num, col_idx,  val, style_info_cell_wrap_on)  
            
            elif attr == 'status':
                sheet1.write(excel_row_num, col_idx,  '%s' % dac.status, style_info_cell_wrap_on)  
            
            elif attr == 'advisors':                
                advisor_str = '\n'.join(map(lambda faculty_member: fmt_faculty_member(faculty_member), dac.current_advisors))
                sheet1.write(excel_row_num, col_idx,  advisor_str, style_info_cell_wrap_on)
            else:
                # default                
                sheet1.write(excel_row_num, col_idx, unicode(dac.__dict__.get(attr,  '')), style_info_cell_wrap_on)  
        
    
    return sheet1
