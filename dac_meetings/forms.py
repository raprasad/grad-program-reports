from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.forms.fields import DateField, ChoiceField, MultipleChoiceField
from django.conf import settings
from dissertation.models import *
from dac_meetings.form_widget import MeetingTypeSelectMultiple
#from tweet_mcb.tweeter import post_new_tweet

MAX_TWEET_SIZE = 140

MEETING_TYPES = "G2Exam G3DAC G4DAC G5DAC G6DAC AdditionalDAC ThesisDefense".split()
MEETING_TYPE_CHOICES = [ (x, x) for x in MEETING_TYPES]

RequiredMeeting.objects.distinct().values_list('meeting_type', flat=True )

class DacForm(forms.Form):
    meeting_type = forms.MultipleChoiceField(required=True\
                    , widget=MeetingTypeSelectMultiple\
                    , initial=MEETING_TYPES\
                    , choices=MEETING_TYPE_CHOICES\
                    )
    
    """message = forms.CharField(label="Enter tweet"\
            , help_text="" 
            , widget=forms.Textarea(attrs={'rows':'2'\
                                , 'style':'width:300px'\
                                , 'class' : 'input-xlarge'\
                                , 'maxlength' : '120'\
                                , 'placeholder' : ''\
                                , 'data-provide' : 'limit'\
                                , 'data-counter' : '#msg_counter'\
                                })\
            )                    
    hashtag = forms.CharField(initial='#MCB_Event')
    link = forms.URLField(initial=''\
                        , required=False\
                        , widget=forms.TextInput(attrs={'size': 50 })\
                        ) 
    """
 
    def get_dac_kwargs(self):
        
        meeting_types = self.cleaned_data.get('meeting_type', None)
        return { 'meeting_type__in' : meeting_types }
        
    def clean(self):
        return self.cleaned_data
        
        full_msg = self.get_full_message()
        if full_msg is None:
            raise forms.ValidationError("Please enter at least a message and a hashtag.")
            
        print 'len(full_msg)', len(full_msg) 
        if len(full_msg) > MAX_TWEET_SIZE:
            err_msg = 'Please reduce the length of your message, hashtag or link'
            self._errors['message'] = self.error_class([err_msg])
            self._errors['hashtag'] = self.error_class([err_msg])
            self._errors['link'] = self.error_class([err_msg])

            raise forms.ValidationError("Your full message is more than %s characters (including links and hashtags).  Please reduce it." % MAX_TWEET_SIZE)
            

        return self.cleaned_data
        
