from django.conf.urls.defaults import *

urlpatterns= patterns(
    'student_requirements.views'    
    , url(r'^requirements/$', 'view_requirements_report', name='view_requirements_report')
    
    , url(r'^requirements/xls/$', 'view_basic_student_report_spreadsheet', name='view_basic_student_report_spreadsheet')
    
    ,
)
