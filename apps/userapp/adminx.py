import xadmin
from userapp.models import *


class CollegeAdmin:
    list_display = ('id', 'name')
    list_per_page = 10  # 每页显示条目数
    ordering = ('id',)  # 按发布日期排序
    model_icon = 'fa fa-university'


class SpecialtyAdmin:
    list_display = ('id', 'name', 'college')
    list_per_page = 10  # 每页显示条目数
    ordering = ('id', 'name',)  # 按发布日期排序
    model_icon = 'fa fa-users'


class SpecialtyTeacherAdmin:
    list_display = ('id', 'specialty', 'teacher')
    list_per_page = 10  # 每页显示条目数
    ordering = ('id', 'specialty',)  # 按发布日期排序
    model_icon = 'glyphicon glyphicon-user'


class TeacherAdmin:
    list_display = ('number', 'name', 'college', 'identity', 'profile_photo')
    list_per_page = 10  # 每页显示条目数
    ordering = ('number', 'name', 'college')  # 按发布日期排序
    model_icon = 'glyphicon glyphicon-user'


class StudentAdmin:
    list_display = ('number', 'name', 'college', 'specialty', 'identity', 'profile_photo', 'total_time')
    list_per_page = 10  # 每页显示条目数
    ordering = ('number', 'name', 'college', 'specialty')  # 按发布日期排序
    model_icon = 'fa fa-graduation-cap'


xadmin.site.register(College, CollegeAdmin)
xadmin.site.register(Specialty, SpecialtyAdmin)
xadmin.site.register(SpecialtyTeacher, SpecialtyTeacherAdmin)
xadmin.site.register(TeacherProfile, TeacherAdmin)
xadmin.site.register(StudentProfile, StudentAdmin)
