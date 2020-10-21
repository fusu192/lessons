import os
import uuid

from django.contrib.auth.hashers import make_password
from django.db import models


class College(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='学院编号')
    name = models.CharField(max_length=30, verbose_name='学院名称')

    class Meta:
        db_table = 'colleges'
        verbose_name = '学院表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Specialty(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='专业编号')
    name = models.CharField(max_length=30, verbose_name='专业名称')
    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name='学院')

    class Meta:
        db_table = 'specialtys'
        verbose_name = '专业表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# Create your models here.
class TeacherProfile(models.Model):
    number = models.CharField(primary_key=True, max_length=20, verbose_name='学号')
    name = models.CharField(max_length=30, verbose_name='姓名')
    password = models.CharField(max_length=200, verbose_name='密码')
    identity = models.CharField(max_length=20, default='teacher', verbose_name='身份', editable=False)  # 学生还是教师
    profile_photo = models.ImageField(upload_to='images/user_profile/',
                                      default='images/user_profile/default/default_teacher.png', editable=False)
    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name='学院')
    specialty = models.ManyToManyField(Specialty, through='SpecialtyTeacher')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if len(self.profile_photo.name) < 32:
            uuid_str = str(uuid.uuid4()).replace('-', '')
            self.profile_photo.name = uuid_str + os.path.splitext(self.profile_photo.name)[-1]
        self.password = make_password(self.password)
        super().save()

    class Meta:
        db_table = 'teacher_profile'
        verbose_name = '教师表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SpecialtyTeacher(models.Model):
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='专业')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, verbose_name='教师')

    class Meta:
        db_table = 'specialty_teacher'
        verbose_name = '专业教师表'
        verbose_name_plural = verbose_name


class StudentProfile(models.Model):
    number = models.CharField(primary_key=True, max_length=20, verbose_name='学号')
    name = models.CharField(max_length=30, verbose_name='姓名')
    password = models.CharField(max_length=200, verbose_name='密码')
    identity = models.CharField(max_length=20, default='student', verbose_name='身份', editable=False)  # 学生还是教师
    total_time = models.CharField(max_length=20, default=0, verbose_name='观看视频总时长', editable=False)
    profile_photo = models.ImageField(upload_to='images/user_profile/',
                                      default='images/user_profile/default/default_student.png', editable=False)
    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name='学院')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='专业')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if len(self.profile_photo.name) < 32:
            uuid_str = str(uuid.uuid4()).replace('-', '')
            self.profile_photo.name = uuid_str + os.path.splitext(self.profile_photo.name)[-1]
        self.password = make_password(self.password)
        super().save()

    class Meta:
        db_table = 'student_profile'
        verbose_name = '学生表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
