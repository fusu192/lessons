from django.core.paginator import Paginator
from django.http import StreamingHttpResponse, JsonResponse, QueryDict
from django.shortcuts import render

# Create your views here.
from django.utils.encoding import escape_uri_path
from django.views import View

from coursewareapp.models import *
from videoapp.models import *


class CoursewareView(View):

    def get(self, request):
        try:
            page_number = request.GET.get('page', default='1')
            number = request.session['user']['number']
            identity = request.session['user']['identity']
            if identity == 'student':
                specialty = StudentProfile.objects.filter(number=number).first().specialty
                # 学生只能看到所在专业的资料
                all_courseware = Courseware.objects.filter(specialty=specialty).all().order_by('-add_time')
            elif identity == 'teacher':
                # 教师只能看见自己发布的资料
                all_courseware = Courseware.objects.filter(teacher_id=number).all()
            paginator = Paginator(all_courseware, 10)  # 实例化分页器对象，第一个参数是数据源，第二个参数是每页显示的条数
            page = paginator.page(page_number)  # 返回page_number页的数据，以Page对象的方式封装该页数据
            return render(request, 'courseware.html', locals())
        except Exception as e:
            print('CoursewareView出错', e)
            return render(request, 'courseware.html')

    def post(self, request):
        pass


# 上传课件
class UploadFile(View):

    def get(self, request):
        print("hahahah")
        return render(request, 'mine.html')

    def post(self, request):
        try:
            courseware_name = request.POST.get('courseware-name')
            courseware_file = request.FILES.get('courseware-file')
            specialty = request.POST.get('courseware-specialty-select')
            print(specialty)
            teacher = request.session['user']['number']
            # 将数据保存到数据库中
            courseware_obj = Courseware.objects.create(name=courseware_name, file=courseware_file, teacher_id=teacher,
                                                       specialty_id=specialty)
            if courseware_obj:
                courseware_obj.save()
                return JsonResponse({'status': 'success'})
            else:
                courseware_obj.delete()
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print('UploadFile出错', e)
            return JsonResponse({'status': 'error'})


# 下载课件
class DownloadFile(View):

    def get(self, request):
        try:
            file_id = request.GET.get('file')
            courseware_obj = Courseware.objects.get(id=file_id)
            courseware_dir = os.path.join(settings.BASE_DIR, 'media/')
            # 拼接路径
            file_path = os.path.join(courseware_dir, str(courseware_obj.file))
            # 拼接下载文件名和格式
            download_path = os.path.join(courseware_obj.name, os.path.splitext(courseware_obj.file.name)[-1])

            # 使用生成器读取文件，可用于读取大文件
            def file_iterator(file_name, chunk_size=512):
                with open(file_name, 'rb') as f:
                    while True:
                        c = f.read(chunk_size)
                        if c:
                            yield c
                        else:
                            break

            response = StreamingHttpResponse(file_iterator(file_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(escape_uri_path(download_path))
            return response
        except Exception as e:
            print('DownloadFile出错', e)
            return render(request, 'courseware.html')

    def post(self, request):
        pass


# 统计下载次数
class DownloadNums(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            courseware_id = request.POST.get('courseware-id')
            courseware_obj = Courseware.objects.filter(id=int(courseware_id))
            # 更新下载次数
            courseware_update_obj = courseware_obj.update(
                download_nums=int(courseware_obj.first().download_nums) + 1)
            if courseware_update_obj:
                return JsonResponse({'status': True})
            else:
                return JsonResponse({'status': False})
        except Exception as e:
            print('DownloadNums出错', e)
            return JsonResponse({'status': False})


class DeleteCourseware(View):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        try:
            delete = QueryDict(request.body)
            courseware_id = delete.get('courseware-id')
            courseware_obj = Courseware.objects.filter(id=courseware_id)
            filename = str(courseware_obj.first().file)
            courseware_delete_obj = courseware_obj.delete()
            if courseware_delete_obj[1]:
                os.remove(os.path.join(settings.BASE_DIR, 'media/' + filename))
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print('DeleteCourseware error:', e)
            return JsonResponse({'status': 'error'})
