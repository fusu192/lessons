from django.db import models

# Create your models here.
from Elearn import settings
from userapp.models import *

file_dir = os.path.join(settings.BASE_DIR, 'media/')

class FileCheck():

    def __init__(self):
        self.file_dir = file_dir

    def get_filesize(self, filename):
        # 获取文件大小（M: 兆）
        file_byte = os.path.getsize(filename)
        filesize = FileCheck.sizeConvert(self, file_byte)
        return filesize

    def sizeConvert(self, size):  # 单位换算
        K, M, G = 1024, 1024 ** 2, 1024 ** 3
        if size >= G:
            return str('%.2f' % (size / G)) + 'G'
        elif size >= M:
            return str('%.2f' % (size / M)) + 'M'
        elif size >= K:
            return str('%.2f' % (size / K)) + 'K'
        else:
            return str('%.2f' % size) + 'B'


class Courseware(models.Model):
    name = models.CharField(max_length=100, verbose_name='课件名称')
    file = models.FileField(upload_to='upload/courseware/%Y%m%d', max_length=200, verbose_name='课件路径')
    size = models.CharField(max_length=20, verbose_name='课件大小', editable=False)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', editable=False)
    download_nums = models.CharField(max_length=10, editable=False, default=0, verbose_name='下载量')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, verbose_name='老师')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='专业')

    class Meta:
        db_table = 'coursewares'
        verbose_name = '课件'
        verbose_name_plural = verbose_name
        ordering = ['add_time']

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if len(self.file.name) < 32:
            uuid_str = str(uuid.uuid4()).replace('-', '')
            self.file.name = uuid_str + os.path.splitext(self.file.name)[-1]
        super().save()
        # 对上传的课件计算大小
        self.size = FileCheck.get_filesize(self, os.path.join(file_dir, str(self.file.name)))
        super().save()

    def delete(self, using=None, keep_parents=False):
        Courseware.objects.filter(id=self.id).delete()
        os.remove(os.path.join(file_dir, str(self.file.name)))
