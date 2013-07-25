import xlwt
from xlwt import easyxf, Formula
from graduate_students.utils.xls_styles import *

from django.core.urlresolvers import reverse
from django.conf import settings
    

def make_faculty_contact_report(sheet1, faculty_members, **kwargs):
    """Spreadsheet for MCB Core admin use"""
    if sheet1 is None:
        return None
    if faculty_members is None:
        return sheet
                  

    #   (header label, attribute, width)
    column_attributes = [ 
     
     ('Last Name', 'last_name', 15)
    ,('First Name', 'first_name', 15)
    ,('is MCO?', 'member_of_training_grant', 10)
    ,('Status', 'status', 10)
    ,('Department', 'department', 20)

    ,('Email', 'email', 25)
    ,('Website', 'website', 25)
    ,('Phone', 'phone', 25)
    ,('Office', 'room', 25)

    ,('Assistant', 'faculty_assistant', 25)
    ,('Assistant Email', 'faculty_assistant.email', 25)
    ,('Assistant Phone', 'faculty_assistant.phone', 25)
    ,('Assistant Office', 'faculty_assistant.room', 25)

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
    for fm in faculty_members:
        excel_row_num +=1

        for col_idx, (col_name, attr, col_width) in enumerate(column_attributes):
            if attr == 'status':
                sheet1.write(excel_row_num, col_idx, '%s' % fm.status, style_info_cell_wrap_on)  
            elif attr == 'member_of_training_grant':
                if fm.member_of_training_grant:
                    val = 'YES'
                else:
                    val = 'no'
                sheet1.write(excel_row_num, col_idx, val, style_info_cell_wrap_on)  
                    
            elif attr == 'faculty_assistant':
                if not fm.faculty_assistant:
                    val = ''
                else:
                    val = '%s' % fm.faculty_assistant
                sheet1.write(excel_row_num, col_idx, val, style_info_cell_wrap_on)  

            elif attr == 'department':
                sheet1.write(excel_row_num, col_idx, '%s' % fm.department, style_info_cell_wrap_on)  
      
            elif attr.startswith('faculty_assistant.'):
                if not fm.faculty_assistant:
                    sheet1.write(excel_row_num, col_idx, '', style_info_cell_wrap_on)  
                    continue
                
                attr_key = attr.replace('faculty_assistant.', '')
                val = fm.faculty_assistant.__dict__.get(attr_key,  '')
                val = '%s' % val
                val = val.encode('ascii', 'ignore')
                    
                sheet1.write(excel_row_num, col_idx, val, style_info_cell_wrap_on)  
            elif attr == 'email':
                if fm.second_email:
                    val = '%s/n%s' % (fm.email, fm.second_email)
                else:
                    val = fm.email
                sheet1.write(excel_row_num, col_idx, val, style_info_cell_wrap_on)  
                
            else:
                # default                
                sheet1.write(excel_row_num, col_idx, unicode(fm.__dict__.get(attr,  '')), style_info_cell_wrap_on)  
        
    
    return sheet1
