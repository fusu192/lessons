# -*- coding: utf-8 -*-
import xadmin
from homeworkapp.models import *


class HomeworkAdmin:
    list_display = ['name','describe', 'add_time', 'answer_nums', 'teacher', 'release']  # 设置列表可显示的字段
    list_per_page = 10  # 每页显示条目数
    ordering = ('name', '-add_time',)  # 按发布日期排序
    model_icon = 'fa fa-book'


class QuestionsAdmin:
    list_display = ['homework', 'question_type', 'context', 'answer', 'add_time', 'teacher']
    list_per_page = 10
    ordering = ('homework', '-add_time')
    model_icon = 'fa fa-question-circle'


class HomeworkSocreAdmin:
    list_display = ['homework', 'pd_score', 'xz_score', 'jd_score']
    list_per_page = 10
    ordering = ('homework',)
    model_icon = 'fa fa-star'


class StudentAnswerLogAdmin:
    list_display = ['student', 'homework', 'question', 'answer', 'score']
    list_per_page = 10
    ordering = ('student', '-score')
    model_icon = 'fa fa-tags'


class StudentScoreAdmin:
    list_display = ['student', 'homework', 'pd_score', 'xz_score', 'jd_score', 'total', 'add_time']
    list_filter = ('add_time',)
    list_per_page = 10
    ordering = ('student', '-total', '-add_time')
    model_icon = 'fa fa-star-half-o'


xadmin.site.register(Homework, HomeworkAdmin)
xadmin.site.register(Questions, QuestionsAdmin)
xadmin.site.register(HomeworkSocre, HomeworkSocreAdmin)
xadmin.site.register(StudentAnswerLog, StudentAnswerLogAdmin)
xadmin.site.register(StudentScore, StudentScoreAdmin)
