from django.urls import path

from elearnapp.views import *

app_name = 'elearnapp'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('home/', Home.as_view(), name='home'),
]
