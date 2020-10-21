from django.urls import path

from coursewareapp.views import *

app_name = 'coursewareapp'

urlpatterns = [
    path('', CoursewareView.as_view(), name='courseware'),
    path('upload/', UploadFile.as_view(), name='upload'),
    path('download/', DownloadFile.as_view(), name='download'),
    path('downloadnums/', DownloadNums.as_view(), name='download_nums'),
    path('deletecourseware/', DeleteCourseware.as_view(), name='delete_courseware')
]
