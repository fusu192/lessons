from django.urls import path

from videoapp.views import *

app_name = 'videoapp'

urlpatterns = [
    path('', AllVideo.as_view(), name='video'),
    path('player/', Player.as_view(), name='player'),
    path('clicknums/', ClickNums.as_view(), name='clicknums'),
    path('counttime/', Counttime.as_view(), name='counttime'),
    path('uploadcourse/', UploadCourse.as_view(), name='uploadcourse'),
    path('uploadvideo/', UploadVideo.as_view(), name='uploadvideo'),
    path('deletevideo/', DeleteVideo.as_view(), name='deletevideo'),
]
