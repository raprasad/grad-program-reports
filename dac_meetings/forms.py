from django import forms
from django.db.models import Max

from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.conf import settings
from dissertation.models import *
from student.models import GraduateStudent, GraduateStudentStatus
#from dac_meetings.form_widget import MeetingTypeSelectMultiple
from datetime import date, timedelta

def get_max_gyear():
    default_max = 7
    max_year = GraduateStudent.objects.all().aggregate(Max('mcb_year'))
    if max_year and max_year.has_key('mcb_year__max'):
        return max_year.get('mcb_year__max', default_max)
    return default_max

MEETING_TYPES = "G2Exam G3DAC G4DAC G5DAC G6DAC AdditionalDAC ThesisDefense".split()
MEETING_TYPE_CHOICES = [ (x, x) for x in MEETING_TYPES]

MEETING_STATUS_CHOICES = [ (status.id, status.name) for status in RequiredMeetingStatus.objects.all()]
MEETING_STATUSES = map(lambda x: x[0], MEETING_STATUS_CHOICES)

STUDENT_STATUS_CHOICES = [ (status.id, status.name) for status in GraduateStudentStatus.objects.all()]
STUDENT_STATUSES = map(lambda x: x[0], STUDENT_STATUS_CHOICES)

GYEARS = range(1, get_max_gyear()+1)
GYEAR_CHOICES = [ (gyear, 'G%s' % gyear ) for gyear in GYEARS]

#GraduateStudent.objects.all().aggregate(Max('mcb_year'))

def get_initial_date(end_date=False):
    if end_date:
        return (date.today() + timedelta(days=365)).strftime('%m/%d/%Y')
        
    return '01/01/2000'#(today + timedelta(days=-180)).strftime('%m/%d/%Y')
    
class DacForm(forms.Form):

    g_year = forms.MultipleChoiceField(required=True\
                    , widget=CheckboxSelectMultiple()\
                    , initial=GYEARS\
                    , choices=GYEAR_CHOICES\
                    )
    
    start_date = forms.DateField(required=True\
                    , initial=get_initial_date()
                    , widget=forms.TextInput(attrs={'style':'width:75px;' }))
    end_date = forms.DateField(required=True\
                                , initial=get_initial_date(end_date=True)
                                , widget=forms.TextInput(attrs={'style':'width:75px;' }))
    nominated_for_prize = forms.BooleanField(label="Prize nominees only", required=False, help_text='')

    meeting_type = forms.MultipleChoiceField(required=True\
                    , widget=CheckboxSelectMultiple()\
                    , initial=MEETING_TYPES\
                    , choices=MEETING_TYPE_CHOICES\
                    )
                    
    meeting_status = forms.MultipleChoiceField(required=True\
                    , widget=CheckboxSelectMultiple()\
                    , initial=MEETING_STATUSES\
                    , choices=MEETING_STATUS_CHOICES\
                            )
   
    student_status = forms.MultipleChoiceField(required=True\
                    , widget=CheckboxSelectMultiple()\
                    , initial=STUDENT_STATUSES[:1]\
                    , choices=STUDENT_STATUS_CHOICES\
                            )

    def get_dac_kwargs(self):
        
        
        dac_kwargs = { 'meeting_type__in' : self.cleaned_data.get('meeting_type', None)\
                , 'status__in' : self.cleaned_data.get('meeting_status')\
                , 'student__status__in' : self.cleaned_data.get('student_status')\
                , 'date__gte' : self.cleaned_data.get('start_date')\
                , 'date__lte' : self.cleaned_data.get('end_date')\
                , 'student__mcb_year__in' : self.cleaned_data.get('g_year')\
         }
        
        if self.cleaned_data.get('nominated_for_prize', None) is True:
            dac_kwargs.update( { 'nominated_for_prize' : True })
            
        return dac_kwargs
        
        
    def clean(self):
        
        start_date = self.cleaned_data.get('start_date', None)
        end_date = self.cleaned_data.get('end_date', None)
        
        if start_date and end_date:
            if end_date < start_date:
                err_msg = 'The end date must be AFTER the start date.'
                self._errors['end_date'] = self.error_class([err_msg])

                raise forms.ValidationError(err_msg)

        return self.cleaned_data
        
