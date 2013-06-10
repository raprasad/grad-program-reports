from django.conf.urls.defaults import *

urlpatterns= patterns(
    'dac_meetings.views'    
    , url(r'^report/$', 'view_dac_meeting_report', name='view_dac_meeting_report')
    
    , url(r'^report/xls/$', 'view_dac_meeting_report_spreadsheet', name='view_dac_meeting_report_spreadsheet')
    
    ,
)
