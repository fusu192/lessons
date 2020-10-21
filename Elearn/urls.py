"""Elearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import handler403, handler404, handler500
from django.conf.urls.static import static
from django.urls import path, include
from django.views.static import serve

import xadmin
from elearnapp.views import page_not_found, page_error, permission_denied


handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error

urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', include('elearnapp.urls', namespace='home')),
    path('video/', include('videoapp.urls', namespace='video')),
    path('courseware/', include('coursewareapp.urls', namespace='courseware')),
    path('homework/', include('homeworkapp.urls', namespace='homework')),
    path('mine/', include('userapp.urls', namespace='mine')),
    path('search/', include('haystack.urls')),
]

urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)  #加上这一行

