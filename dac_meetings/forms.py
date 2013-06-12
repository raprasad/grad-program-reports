from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.conf import settings
from dissertation.models import *
#from dac_meetings.form_widget import MeetingTypeSelectMultiple
from datetime import date, timedelta

MEETING_TYPES = "G2Exam G3DAC G4DAC G5DAC G6DAC AdditionalDAC ThesisDefense".split()
MEETING_TYPE_CHOICES = [ (x, x) for x in MEETING_TYPES]

RequiredMeeting.objects.distinct().values_list('meeting_type', flat=True )

def get_initial_date(end_date=False):
    today = date.today()
    if end_date:
        return (today + timedelta(days=50)).strftime('%m/%d/%Y')
        
    return (today + timedelta(days=-180)).strftime('%m/%d/%Y')
    
class DacForm(forms.Form):
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
    
   
    def get_dac_kwargs(self):
        
        
        dac_kwargs = { 'meeting_type__in' : self.cleaned_data.get('meeting_type', None)\
                , 'date__gte' : self.cleaned_data.get('start_date')
                , 'date__lte' : self.cleaned_data.get('end_date')
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
        
