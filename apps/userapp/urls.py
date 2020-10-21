from django.urls import path

from userapp.views import *

app_name = 'userapp'

urlpatterns = [
    path('', Mine.as_view(), name='mine'),
    path('teacherregister/', TeacherReg.as_view(), name='teacherregister'),
    path('teacherlogin/', TeacherLog.as_view(), name='teacherlogin'),
    path('studentregister/', StudentReg.as_view(), name='studentregister'),
    path('studentlogin/', StudentLog.as_view(), name='studentlogin'),
    path('resetpassword/',ResetPassword.as_view(), name='resetpassword'),
    path('headpicture/',HeadPicture.as_view(), name='headpicture'),
    path('specialty/', SelectSpecialty.as_view(), name='specialty'),
    path('loginout/', LoginOut.as_view(), name='loginout'),
]
