import json

from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from homeworkapp.models import *
from userapp.models import *
from videoapp.models import *


class Mine(View):

    def get(self, request):
        try:
            if request.session['user']['identity'] == 'student':
                stu = request.session['user']['number']
                s_score = StudentScore.objects.filter(student_id=stu)
                total = StudentProfile.objects.filter(number=stu).first().total_time
                total_time = FileCheck.timeConvert(self, int(total))
            elif request.session['user']['identity'] == 'teacher':
                teacher = request.session['user']['number']
                print(teacher)
                all_course = Course.objects.filter(teacher_id=teacher).all()
                all_homework = Homework.objects.filter(teacher_id=teacher).all()
                my_homework = Homework.objects.filter(teacher_id=teacher).all()
                college = TeacherProfile.objects.filter(number=teacher).first().college_id
                specialtys = SpecialtyTeacher.objects.filter(teacher_id=teacher).all()  # 该教师教授专业
                all_student_details = []
                for specialty in specialtys:
                    all_student_details.append(
                        StudentProfile.objects.filter(specialty_id=specialty.specialty_id).all())  # 该教师教授所有专业所有学生学习情况
                all_student_score = StudentScore.objects.all()
                student_list = []
                for student in all_student_details:
                    for student2 in student:
                        s = []
                        l = []
                        one_time = FileCheck.timeConvert(self, int(student2.total_time))
                        s.append(student2.name)
                        s.append(student2.specialty)
                        s.append(one_time)
                        l.append(s)
                        student_list.extend(l)
            return render(request, 'mine.html', locals())
        except Exception as e:
            print(e)
            return render(request, 'mine.html')

    def post(self, request):
        pass


class TeacherReg(View):

    def get(self, request):
        pass

    def post(self, request):
        name = request.POST.get('name')
        number = request.POST.get('number')
        password = request.POST.get('password')
        identity = request.POST.get('identity')
        code = request.POST.get('code')
        college = request.POST.get('college')
        try:
            if code == '123456':
                teacher = TeacherProfile.objects.filter(number=number).first()  # 判断学号是否存在
                if teacher:
                    return JsonResponse({'status': 'error', 'code': 'ok'})  # 验证正确但学号存在
                else:
                    # 不存在新建
                    new_teacher = TeacherProfile.objects.create(number=number, name=name, password=password,
                                                                identity=identity, college_id=college)
                    if new_teacher:
                        request.session['user'] = {
                            'number': new_teacher.number,
                            'name': new_teacher.name,
                            'identity': new_teacher.identity,
                            'photo': json.dumps(str(new_teacher.profile_photo))[1:-1],
                        }  # 将信息保存到session中
                        request.session.set_expiry(60 * 60 * 24)  # session失效时间
                        return JsonResponse({'status': 'ok', 'code': 'ok'})
                    else:
                        new_teacher.delete()  # 出错删除
                        return JsonResponse({'status': 'stop'})  # 服务器出错
            else:
                return JsonResponse({'code': 'error'})  # 注册码不正确
        except Exception as e:
            print('注册出错啦：', e)
            return JsonResponse({'status': 'stop'})  # 服务器出错


class TeacherLog(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            number = request.POST.get('number')
            password = request.POST.get('password')
            teacher = TeacherProfile.objects.filter(number=number).first()  # 判断是否存在
            if teacher:
                if check_password(password, teacher.password):  # 密码认证:
                    request.session['user'] = {
                        'number': teacher.number,
                        'name': teacher.name,
                        'identity': teacher.identity,
                        'photo': json.dumps(str(teacher.profile_photo))[1:-1],
                    }
                    request.session.set_expiry(60 * 60 * 24)  # session失效时间
                    return JsonResponse({'status': 'log_ok'})
                else:
                    return JsonResponse({'status': 'log_error'})  # 密码错误
            else:
                return JsonResponse({'status': 'log_empty'})  # 学号不存在
        except Exception as e:
            print("登录出错啦：", e)
            return JsonResponse({'status': 'log_stop'})  # 服务器出错


class StudentReg(View):

    def get(self, request):
        pass

    def post(self, request):
        name = request.POST.get('name')
        number = request.POST.get('number')
        password = request.POST.get('password')
        identity = request.POST.get('identity')
        college = request.POST.get('college')
        specialty = request.POST.get('specialty')
        try:
            student = StudentProfile.objects.filter(number=number).first()  # 判断学号是否存在
            if student:
                return JsonResponse({'status': 'error'})  # 学号存在
            else:
                # 不存在新建
                new_student = StudentProfile.objects.create(number=number, name=name, password=password,
                                                            identity=identity, college_id=college,
                                                            specialty_id=specialty)
                if new_student:
                    request.session['user'] = {
                        'number': new_student.number,
                        'name': new_student.name,
                        'identity': new_student.identity,
                        'photo': json.dumps(str(new_student.profile_photo))[1:-1],
                    }  # 将信息保存到session中
                    request.session.set_expiry(60 * 60 * 24)  # session失效时间
                    return JsonResponse({'status': 'ok'})
                else:
                    new_student.delete()  # 出错删除
                    return JsonResponse({'status': 'stop'})  # 服务器出错
        except Exception as e:
            print('注册出错啦：', e)
            return JsonResponse({'status': 'stop'})  # 服务器出错


class StudentLog(View):

    def get(self, request):
        pass

    def post(self, request):
        number = request.POST.get('number')
        password = request.POST.get('password')
        try:
            student = StudentProfile.objects.filter(number=number).first()  # 判断是否存在
            if student:
                if check_password(password, student.password):  # 密码认证
                    request.session['user'] = {
                        'number': student.number,
                        'name': student.name,
                        'identity': student.identity,
                        'photo': json.dumps(str(student.profile_photo))[1:-1],
                    }
                    request.session.set_expiry(60 * 60 * 24)  # session失效时间
                    return JsonResponse({'status': 'log_ok'})
                else:
                    return JsonResponse({'status': 'log_error'})  # 密码错误
            else:
                return JsonResponse({'status': 'log_empty'})  # 学号不存在
        except Exception as e:
            print("登录出错啦：", e)
            return JsonResponse({'status': 'log_stop'})  # 服务器出错


class ResetPassword(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            password = request.POST.get('password')
            number = request.session['user']['number']
            identity = request.session['user']['identity']
            if identity == 'student':
                student_obj = StudentProfile.objects.filter(number=number)
                if check_password(password, student_obj.first().password):
                    return JsonResponse({'status': 'same'})
                else:
                    student = student_obj.update(password=make_password(password))
                    if student:
                        request.session['user'] = {
                            'number': student_obj.first().number,
                            'name': student_obj.first().name,
                            'identity': student_obj.first().identity,
                            'specialty': student_obj.first().specialty,
                            'photo': json.dumps(str(student_obj.first().profile_photo))[1:-1],
                        }
                        return JsonResponse({'status': 'success'})
                    else:
                        return JsonResponse({'status': 'error'})
            elif identity == 'teacher':
                teacher_obj = TeacherProfile.objects.filter(number=number)
                if check_password(password, teacher_obj.first().password):
                    return JsonResponse({'status': 'same'})
                else:
                    teacher = teacher_obj.update(password=make_password(password))
                    if teacher:
                        request.session['user'] = {
                            'number': teacher_obj.first().number,
                            'name': teacher_obj.first().name,
                            'identity': teacher_obj.first().identity,
                            'photo': json.dumps(str(teacher_obj.first().profile_photo))[1:-1],
                        }
                        return JsonResponse({'status': 'success'})
                    else:
                        return JsonResponse({'status': 'error'})
        except Exception as e:
            print("ResetPassword error:", e)
            return JsonResponse({'status': 'stop'})  # 服务器出错


class HeadPicture(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            head_picture = request.FILES.get('head-picture')
            number = request.session['user']['number']
            identity = request.session['user']['identity']
            photo_dir = os.path.join(settings.BASE_DIR, 'static/')
            uuid_str = str(uuid.uuid4()).replace('-', '')
            file_name = os.path.join('images/user_profile/', uuid_str + os.path.splitext(head_picture.name)[-1])
            profile_photo = ''
            with open(os.path.join(photo_dir, file_name), 'wb') as f:
                for chunk in head_picture.chunks():
                    f.write(chunk)
            if identity == 'student':
                student_obj = StudentProfile.objects.filter(number=number)
                if str(student_obj.first().profile_photo) != str('images/user_profile/default/default_student.png'):
                    profile_photo = os.path.join(photo_dir, str(student_obj.first().profile_photo))
                student = student_obj.update(profile_photo=file_name)
                if student:
                    if profile_photo:
                        os.remove(profile_photo)
                    request.session['user'] = {
                        'number': student_obj.first().number,
                        'name': student_obj.first().name,
                        'identity': student_obj.first().identity,
                        'photo': json.dumps(str(student_obj.first().profile_photo))[1:-1],
                    }
                    return JsonResponse({'status': 'success', "photo": file_name})
                else:
                    return JsonResponse({'status': 'error'})
            elif identity == 'teacher':
                teacher_obj = TeacherProfile.objects.filter(number=number)
                if str(teacher_obj.first().profile_photo) != 'images/user_profile/default/default_teacher.png':
                    profile_photo = os.path.join(photo_dir, str(teacher_obj.first().profile_photo))
                teacher = teacher_obj.update(profile_photo=file_name)
                if teacher:
                    if profile_photo:
                        os.remove(profile_photo)
                    request.session['user'] = {
                        'number': teacher_obj.first().number,
                        'name': teacher_obj.first().name,
                        'identity': teacher_obj.first().identity,
                        'photo': json.dumps(str(teacher_obj.first().profile_photo))[1:-1],
                    }
                    return JsonResponse({'status': 'success', "photo": file_name})
                else:
                    return JsonResponse({'status': 'error'})
        except Exception as e:
            print("HeadPicture error:", e)
            return JsonResponse({'status': 'stop'})  # 服务器出错


class SelectSpecialty(View):

    def get(self, request):
        try:
            college = request.GET.get('college')
            specialty_obj = Specialty.objects.filter(college_id=college).all()
            specialty_list = []
            for s in specialty_obj:
                specialty = {}
                specialty['id'] = s.id
                specialty['name'] = s.name
                specialty_list.append(specialty)
            return JsonResponse({'data': specialty_list})
        except Exception as e:
            print('SelectSpecialty error:', e)

    def post(self, request):
        pass


class LoginOut(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('home:home'))

    def post(self, request):
        pass
