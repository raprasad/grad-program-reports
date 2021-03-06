from django import forms
from django.db.models import Max

from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.conf import settings
from dissertation.models import *
from graduate_students.department.models import Department
from graduate_students.faculty.models import FacultyMember, FacultyStatus

#from dac_meetings.form_widget import MeetingTypeSelectMultiple
from datetime import date, timedelta

def get_mco_faculty_depts():
    
    mco_dept_ids = FacultyMember.objects.filter(is_active=True\
                            , member_of_training_grant=True\
                        ).values_list('department__id', flat=True)
    selected_department_choices = map(lambda x: x.id, Department.objects.filter(id__in=mco_dept_ids))
    return selected_department_choices
    
FACULTY_STATUS_CHOICES = [ (status.id, status.name) for status in FacultyStatus.objects.all()]
FACULTY_STATUS_SELECTED = map(lambda x: x.id, FacultyStatus.objects.filter(is_active_status=True))

DEPARTMENT_CHOICES = [ (dept.id, '%s' % dept ) for dept in Department.objects.all()]
DEPARTMENT_DEFAULT_SETTIGNGS = get_mco_faculty_depts()


class ContactForm(forms.Form):

    is_mco = forms.BooleanField(label="MCO faculty only"\
                                , required=False\
                                , initial=True\
                                , help_text='')

    faculty_status = forms.MultipleChoiceField(required=True\
                    , widget=CheckboxSelectMultiple()\
                    , choices=FACULTY_STATUS_CHOICES\
                    , initial=FACULTY_STATUS_SELECTED\
                    )

    department = forms.MultipleChoiceField(required=True\
                    , widget=CheckboxSelectMultiple(attrs={'size': 12})\
                    , choices=DEPARTMENT_CHOICES\
                    , initial=DEPARTMENT_DEFAULT_SETTIGNGS\
                    )


    def get_faculty_info_kwargs(self):
        
        faculty_kwargs = { 'department__in' : self.cleaned_data.get('department', None)\
                , 'status__in' : self.cleaned_data.get('faculty_status')\
         }
        
        if self.cleaned_data.get('is_mco', None) is True:
            faculty_kwargs.update( { 'member_of_training_grant' : True })
            
        return faculty_kwargs
        