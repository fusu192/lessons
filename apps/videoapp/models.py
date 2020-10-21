import os
import time
import uuid

from django.db import models

# Create your models here.
# 课程模型
from moviepy.editor import VideoFileClip

from Elearn import settings
from userapp.models import TeacherProfile


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='课程标题')
    cover = models.ImageField(upload_to='upload/cover/%Y%m%d', max_length=200, verbose_name='课程封面')
    describe = models.CharField(max_length=300, verbose_name='课程描述', blank=True)
    click_nums = models.IntegerField(default=0, verbose_name="点击量", editable=False)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, verbose_name='教师')  # 关联课程发布者

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if len(self.cover.name) < 32:
            uuid_str = str(uuid.uuid4()).replace('-', '')
            self.cover.name = uuid_str + os.path.splitext(self.cover.name)[-1]
        super().save()

    def delete(self, using=None, keep_parents=False):
        video = Video.objects.filter(course_id=self.id).all()
        if video is not None:
            for v in video:
                os.remove(os.path.join(file_dir, str(v.file.name)))
            Course.objects.filter(id=self.id).delete()
            os.remove(os.path.join(file_dir, str(self.cover.name)))
        else:
            Course.objects.filter(id=self.id).delete()
            os.remove(os.path.join(file_dir, str(self.cover.name)))

    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = verbose_name
        ordering = ['click_nums']

    def __str__(self):
        return self.title


# 计算视频时长
file_dir = os.path.join(settings.BASE_DIR, 'media/')


class FileCheck():
    def __init__(self):
        self.file_dir = file_dir

    def get_file_times(self, filename):
        clip = VideoFileClip(filename)
        file_time = FileCheck.timeConvert(self, clip.duration)
        clip.close()
        return file_time

    def timeConvert(self, size):  # 单位换算
        M, H = 60, 60 ** 2
        if size < M:
            return str(size) + u'秒'
        if size < H:
            return u'%s分钟%s秒' % (int(size / M), int(size % M))
        else:
            hour = int(size / H)
            mine = int(size % H / M)
            second = int(size % H % M)
            tim_srt = u'%s小时%s分钟%s秒' % (hour, mine, second)
            return tim_srt


# 视频模型
class Video(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)  # 关联课程
    title = models.CharField(max_length=100, verbose_name='视频标题')
    file = models.FileField(upload_to='upload/video/%Y%m%d', max_length=200, verbose_name='视频')
    duration = models.CharField(max_length=30, verbose_name='视频时长', default=0, editable=False)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 对上传视频进行重命名
        if len(self.file.name) < 32:
            uuid_str = str(uuid.uuid4()).replace('-', '')
            self.file.name = uuid_str + os.path.splitext(self.file.name)[-1]
        super().save()
        # 对上传的视频计算时长
        self.duration = FileCheck.get_file_times(self, os.path.join(file_dir, str(self.file.name)))
        super().save()

    def delete(self, using=None, keep_parents=False):
        Video.objects.filter(id=self.id).delete()
        os.remove(os.path.join(file_dir, str(self.file.name)))

    class Meta:
        db_table = 'videos'
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
