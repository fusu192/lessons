from django.core.paginator import Paginator
from django.http import JsonResponse,  QueryDict
from django.shortcuts import render

# Create your views here.
from django.views import View

from userapp.models import *
from videoapp.models import *


# 所有视频
class AllVideo(View):
    def get(self, request):
        page_num = request.GET.get('page', default='1')
        page_num = int(page_num)
        try:
            all_course = Course.objects.all().order_by('-add_time')  # 按时间降序排序
            all_course_list = []
            for course in all_course:
                if course.video_set.count():  # 挑选出关联有视频的课程
                    all_course_list.append(course)
            paginator = Paginator(all_course_list, 8)  # 实例化分页器对象，第一个参数是数据源，第二个参数是每页显示的条数
            page = paginator.page(page_num)  # 返回page_number页的数据，以Page对象的方式封装该页数据
            if page_num < 3:
                if paginator.num_pages <= 4:
                    dis_range = range(1, paginator.num_pages + 1)
                else:
                    dis_range = range(1, 5)
            elif (page_num >= 3) and (page_num <= paginator.num_pages - 2):
                dis_range = range(page_num - 2, page_num + 2)
            else:
                dis_range = range(paginator.num_pages - 2, paginator.num_pages + 1)
            return render(request, 'video.html', locals())
        except Exception as e:
            print(e)
            return render(request, 'video.html')

    def post(self, request):
        pass


# 播放视频
class Player(View):
    def get(self, request):
        try:
            courseid = request.GET.get('course')
            videoid = request.GET.get('videoid')
            courseid = int(courseid)
            videoid = int(videoid)
            course_obj = Course.objects.filter(id=courseid).first()
            video_obj = Video.objects.filter(course_id=courseid).all()  # 该课程的所有视频
            first_video = Video.objects.filter(id=videoid).first()  # 默认播放第一个视频
            return render(request, 'video_player.html', locals())
        except Exception as e:
            print(e)
            return render(request, 'video_player.html', locals())


# 统计点击量
class ClickNums(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            course_id = request.POST.get('course-id')
            course_obj = Course.objects.filter(id=course_id)
            course_update_obj = course_obj.update(click_nums=int(course_obj.first().click_nums) + 1)
            if course_update_obj:
                return JsonResponse({'status': True})
            else:
                return JsonResponse({'status': False})
        except Exception as e:
            print(e)
            return JsonResponse({'status': False})


# 统计学生播放视频时间
class Counttime(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            sTime = request.POST.get('sTime')
            if request.session['user']['identity'] == 'student':
                number = request.session['user']['number']
                studentobj = StudentProfile.objects.filter(number=number)
                if studentobj:
                    total_time = studentobj.first().total_time
                    new_total_time = int(total_time) + int(sTime)
                    s_update_obj = studentobj.update(total_time=new_total_time)
                    if s_update_obj:
                        return JsonResponse({"sTime": sTime + "秒"})
                    else:
                        return JsonResponse({"sTime": "error"})
                else:
                    return JsonResponse({"sTime": "error"})
            else:
                return JsonResponse({"sTime": "error"})
        except Exception as e:
            print(e)
            return JsonResponse({"sTime": "error"})


# 增加课程
class UploadCourse(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            course_name = request.POST.get('course-name')
            course_desc = request.POST.get('course-desc')
            course_file = request.FILES.get('course-file')
            teacher = request.session['user']['number']
            if course_desc == '':
                course_desc = '无'
            course_obj = Course.objects.create(title=course_name, cover=course_file, describe=course_desc,
                                               teacher_id=teacher)
            if course_obj:
                course_obj.save()
                return JsonResponse({'status': 'success'})
            else:
                course_obj.delete()
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'})


# 增加视频
class UploadVideo(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            course_select = request.POST.get('course-select')
            video_title = request.POST.get('video-title')
            video_file = request.FILES.get('video-file')
            video_obj = Video.objects.create(course_id=int(course_select), title=video_title, file=video_file)
            if video_obj:
                video_obj.save()
                return JsonResponse({'status': 'success'})
            else:
                video_obj.delete()
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'})


class DeleteVideo(View):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        try:
            delete = QueryDict(request.body)
            video_id = delete.get('video-id')
            course_id = delete.get('course-id')
            video_obj = Video.objects.filter(id=video_id)
            course = Course.objects.filter(id=course_id)
            filename = str(video_obj.first().file)
            video_delete_obj = video_obj.delete()
            if video_delete_obj[1]:
                os.remove(os.path.join(settings.BASE_DIR, 'media/' + filename))
                if course.first().video_set.count() == 0:
                    covername = str(course.first().cover)
                    course_delete_obj = course.delete()
                    if course_delete_obj[1]:
                        os.remove(os.path.join(settings.BASE_DIR, 'media/' + covername))
                        return JsonResponse({'status': 'remove'})
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print('DeleteVideo error:', e)
            return JsonResponse({'status': 'error'})
