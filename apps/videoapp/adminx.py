import xadmin
from videoapp.models import *


class CourseAdmin:
    list_display = ('title', 'cover', 'describe', 'click_nums', 'add_time', 'teacher')
    list_per_page = 10  # 每页显示条目数
    ordering = ('title', '-add_time',)  # 按发布日期排序
    model_icon = 'glyphicon glyphicon-list-alt'


class VideoAdmin:
    list_display = ('course', 'title', 'file', 'duration', 'add_time')
    list_per_page = 10  # 每页显示条目数
    ordering = ('course', 'title', '-add_time',)  # 按发布日期排序
    model_icon = 'fa fa-film'


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Video, VideoAdmin)
