from django.conf.urls.defaults import *

urlpatterns= patterns(
    'faculty_info.views'    
    , url(r'^contact-info/$', 'view_faculty_contacts', name='view_faculty_contacts')
    
    #, url(r'^contact-info/xls/$', 'view_faculty_assistants_spreadsheet', name='view_faculty_assistants_spreadsheet')
    
    ,
)
