from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View

from homeworkapp.models import *


class HomeworkView(View):

    def get(self, request):
        try:
            page_number = request.GET.get('page', default='1')
            number = request.session['user']['number']
            identity = request.session['user']['identity']
            # 挑选出已发布的所有作业
            if identity == 'student':
                specialty = StudentProfile.objects.filter(number=number).first().specialty
                all_homework = Homework.objects.filter(specialty=specialty).all()
            elif identity == 'teacher':
                all_homework = Homework.objects.filter(teacher_id=number, release=True).all()
            all_homework_list = []
            for h in all_homework:
                if h.questions_set.all():
                    all_homework_list.append(h)
            paginator = Paginator(all_homework_list, 10)  # 实例化分页器对象，第一个参数是数据源，第二个参数是每页显示的条数
            page = paginator.page(page_number)  # 返回page_number页的数据，以Page对象的方式封装该页数据
            return render(request, 'homework.html', locals())
        except Exception as e:
            print(e)
            return render(request, 'homework.html')

    def post(self, request):
        pass


# 该作业中的所有题目
class Details(View):

    def get(self, request):
        h_id = request.GET.get('list')
        questions = Questions.objects.filter(homework_id=h_id)  # 根据作业id挑选出当前作业的所有问题
        pd_list = []
        xz_list = []
        jd_list = []
        for q in questions:
            if q.question_type == 'pd':
                pd_list.append(q)
            elif q.question_type == 'xz':
                xz_list.append(q)
            elif q.question_type == 'jd':
                jd_list.append(q)
        return render(request, 'homework_details.html', locals())

    def post(self, request):
        pass


class Judge(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            homework_id = request.POST.get('h')  # 获取作业id
            student_number = request.session['user']['number']  # 获取登录学生学号
            student_score = StudentScore.objects.filter(student_id=student_number,
                                                        homework_id=homework_id).first()  # 判断是否已提交作业
            if student_score is None:  # 未提交才可执行
                homework_obj = Homework.objects.filter(id=homework_id)  # 根据作业id挑选出当前作业对象
                questions = Questions.objects.filter(homework=homework_obj.first()).all()  # 根据作业对象挑选出当前作业的所有问题
                homework_score = HomeworkSocre.objects.filter(homework=homework_obj.first()).first()
                pd = questions.filter(question_type='pd').all()  # 挑选出所有判断题
                xz = questions.filter(question_type='xz').all()  # 挑选出所有选择题
                jd = questions.filter(question_type='jd').all()  # 挑选出所有简答题
                pd_score = 0
                if homework_score is None:
                    homework_score = HomeworkSocre.objects.create(homework=homework_obj.first())  # 没有设置作业分数时
                for i, p in enumerate(pd):
                    pd_a = request.POST.get(str(p.id))  # 根据题目id获取学生的答案
                    pd_obj = pd[i]
                    if pd_obj.answer == pd_a:
                        pd_score += 1
                        # 添加做题日志
                        pd_log = StudentAnswerLog.objects.create(student_id=student_number, homework_id=homework_id,
                                                                 question=pd_obj, answer=pd_a,
                                                                 score=homework_score.pd_score, question_type='pd')
                        pd_log.save()
                    else:
                        pd_score += 0
                        pd_log1 = StudentAnswerLog.objects.create(student_id=student_number, homework_id=homework_id,
                                                                  question=pd_obj, answer=pd_a, score=0,
                                                                  question_type='pd')
                        pd_log1.save()
                pd_score *= homework_score.pd_score  # 判断题总分

                xz_score = 0
                for j, x in enumerate(xz):
                    xz_a = request.POST.get(str(x.id))  # 根据题目id获取学生的答案
                    xz_obj = xz[j]
                    if xz_obj.answer == xz_a:
                        xz_score += 1
                        xz_log1 = StudentAnswerLog.objects.create(student_id=student_number, homework_id=homework_id,
                                                                  question=xz_obj, answer=xz_a,
                                                                  score=homework_score.xz_score, question_type='xz')
                        xz_log1.save()
                    else:
                        xz_score += 0
                        xz_log2 = StudentAnswerLog.objects.create(student_id=student_number, homework_id=homework_id,
                                                                  question=xz_obj, answer=xz_a, score=0,
                                                                  question_type='xz')
                        xz_log2.save()
                xz_score *= homework_score.xz_score  # 选择题总分

                for k, j in enumerate(jd):
                    jd_a = request.POST.get(str(j.id))  # 根据题目id获取学生的答案
                    jd_obj = jd[k]
                    jd_log = StudentAnswerLog.objects.create(student_id=student_number, homework_id=homework_id,
                                                             question=jd_obj, answer=jd_a, question_type='jd')
                    jd_log.save()
                total = pd_score + xz_score  # 判断题加选择分数
                s = StudentScore.objects.create(student_id=student_number, homework=homework_obj.first(),
                                                pd_score=pd_score, xz_score=xz_score, total=total)

                if s:
                    s.save()
                    homework_update_obj = homework_obj.update(answer_nums=int(homework_obj.first().answer_nums) + 1)
                    return redirect(reverse('homework:homework'))
            else:
                return redirect(reverse('homework:homework'))

        except Exception as e:
            print(e)
            return redirect(reverse('homework:homework'))


# 检查学生是否已提交作业
class Check(View):

    def get(self, request):
        homework_id = request.GET.get('h')  # 获取作业id
        number = request.session['user']['number']  # 获取已登录学生id
        s = StudentScore.objects.filter(student_id=number, homework_id=homework_id)  # 判断是否已提交作业
        if s:
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})

    def post(self, request):
        pass


# 增加作业
class UploadHomework(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            homework_name = request.POST.get('homework-name')
            homework_desc = request.POST.get('homework-desc')
            specialty = request.POST.get('homework-specialty-select')
            teacher = request.session['user']['number']
            if homework_desc == '':
                homework_desc = '无'
            homework_obj = Homework.objects.create(name=homework_name, describe=homework_desc,
                                                   teacher_id=teacher, specialty_id=specialty)
            if homework_obj:
                homework_obj.save()
                return JsonResponse({'status': 'success'})
            else:
                homework_obj.delete()
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'})


# 增加判断题
class AddPDQuestion(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            homework_id = request.POST.get('homework')
            pd_question = request.POST.get('pd-question')
            pd_answer = request.POST.get('pd-answer')
            teacher = request.session['user']['number']
            questions_obj = Questions.objects.create(homework_id=homework_id, teacher_id=teacher, question_type='pd',
                                                     context=pd_question, choice_a='', choice_b='',
                                                     choice_c='', choice_d='', answer=pd_answer)
            if questions_obj:
                questions_obj.save()
                return JsonResponse({'status': 'success'})
            else:
                questions_obj.delete()
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'})


# 增加选择题
class AddXZQuestion(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            homework_id = request.POST.get('homework')
            xz_question = request.POST.get('xz-question')  # 获取题目
            xz_answer_A = request.POST.get('xz-answer-A')  # 获取选项内容
            xz_answer_B = request.POST.get('xz-answer-B')
            xz_answer_C = request.POST.get('xz-answer-C')
            xz_answer_D = request.POST.get('xz-answer-D')
            xz_answer = request.POST.get('xz-answer')  # 获取答案
            teacher = request.session['user']['number']
            questions_obj = Questions.objects.create(homework_id=homework_id, teacher_id=teacher, question_type='xz',
                                                     context=xz_question, choice_a=xz_answer_A, choice_b=xz_answer_B,
                                                     choice_c=xz_answer_C, choice_d=xz_answer_D, answer=xz_answer)
            if questions_obj:
                questions_obj.save()
                return JsonResponse({'status': 'success'})
            else:
                questions_obj.delete()
                return JsonResponse({'status': 'error'})
        except Exception as e:
            return JsonResponse({'status': 'error'})


# 增加简答题
class AddJDQuestion(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            homework_id = request.POST.get('homework')
            jd_question = request.POST.get('jd-question')
            jd_answer = request.POST.get('jd-answer')
            teacher = request.session['user']['number']
            questions_obj = Questions.objects.create(homework_id=homework_id, teacher_id=teacher, question_type='jd',
                                                     context=jd_question, choice_a='', choice_b='',
                                                     choice_c='', choice_d='', answer=jd_answer)
            if questions_obj:
                questions_obj.save()
                return JsonResponse({'status': 'success'})
            else:
                questions_obj.delete()
                return JsonResponse({'status': 'error'})
        except Exception as e:
            return JsonResponse({'status': 'error'})


# 发布作业
class Release(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            homework_id = request.POST.get('homeworkid')
            homework_obj = Homework.objects.filter(id=homework_id)
            if homework_obj:
                homework_update_obj = homework_obj.update(release=1)
                if homework_update_obj:
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'error'})
            else:
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error'})


# 获取已提交作业的学生
class ReleaseStudent(View):

    def get(self, request):
        homework_id = request.GET.get('homework-id')
        studentscore = StudentScore.objects.filter(homework_id=int(homework_id)).all()
        data = []
        for s in studentscore:
            sp = StudentProfile.objects.filter(number=s.student_id).first()
            data.append(sp)
        return JsonResponse({'data': serializers.serialize('json', data)})

    def post(self, request):
        pass


# 批改简答题
class Correct(View):

    def get(self, request):
        student_id = request.GET.get('studentid')
        homework_id = request.GET.get('homeworkid')
        SAL_obj = StudentAnswerLog.objects.filter(student_id=student_id, homework_id=homework_id)
        pd_list = []
        xz_list = []
        jd_list = []
        for sal in SAL_obj:
            if sal.question_type == 'pd':
                pd_list.append(sal)
            elif sal.question_type == 'xz':
                xz_list.append(sal)
            elif sal.question_type == 'jd':
                jd_list.append(sal)
        return render(request, 'homework_correct.html', locals())

    def post(self, request):
        try:
            studentid = request.POST.get('studentid')
            homework_id = request.POST.get('homeworkid')
            all_studentanswerlog = StudentAnswerLog.objects.filter(student_id=studentid,
                                                                   homework_id=homework_id).all()  # 获取学生答题记录对象
            jd_score = 0  # 简答题总分
            for i, s in enumerate(all_studentanswerlog):
                if s.question_type == 'jd':
                    qid = request.POST.get(str(s.question_id))
                    qscore = request.POST.get('score' + str(s.question_id))  # 接收所得分数
                    question_obj = all_studentanswerlog.filter(question_id=qid)  # 获取题目对象
                    if question_obj:
                        question_update_obj = question_obj.update(score=qscore)  # 更新简答题分数
                        jd_score += int(qscore)
            studentscore_obj = StudentScore.objects.filter(student_id=studentid, homework_id=homework_id)  # 获取学生分数对象
            if studentscore_obj:
                studentscore_update_obj = studentscore_obj.update(jd_score=jd_score)
                if studentscore_update_obj:
                    studentscore = studentscore_obj.first()
                    studentscore_update_obj = studentscore_obj.update(
                        total=int(studentscore.pd_score) + int(studentscore.xz_score) + int(studentscore.jd_score),
                        correct=1)  # 更新作业总分和公布答案
            return redirect(reverse('homework:homework'))
        except Exception as e:
            print(e)
            return redirect(reverse('mine:mine'))


# 公布答案
class Answer(View):

    def get(self, request):
        homework_id = request.GET.get('hid')
        student_id = request.session['user']['number']
        questions_obj = Questions.objects.filter(homework_id=homework_id)
        studentanswerlog_obj = StudentAnswerLog.objects.filter(homework_id=homework_id, student_id=student_id)
        pd_list = []  # 正确答案
        xz_list = []
        jd_list = []
        my_pd_list = []  # 我的答案
        my_xz_list = []
        my_jd_list = []
        for question in questions_obj:
            my_answer = studentanswerlog_obj.filter(question_id=question.id).first().answer
            if question.question_type == 'pd':
                pd_list.append(question)  # 题目及答案
                my_pd_list.append(my_answer)  # 学生答案
            elif question.question_type == 'xz':
                xz_list.append(question)
                my_xz_list.append(my_answer)
            elif question.question_type == 'jd':
                jd_list.append(question)
                my_jd_list.append(my_answer)
        return render(request, 'answer.html', locals())

    def post(self, request):
        pass


# 修改题目
class Modification(View):

    def get(self, request):
        homework_id = request.GET.get('id')
        questions_obj = Questions.objects.filter(homework_id=homework_id).all()
        pd_question_list = []
        xz_question_list = []
        jd_question_list = []
        for question in questions_obj:
            if question.question_type == 'pd':
                pd_question = []
                pd_question.extend((question.id, question.context, question.answer))
                pd_question_list.append(pd_question)
            elif question.question_type == 'xz':
                xz_question = []
                xz_question.extend((question.id, question.context, question.choice_a, question.choice_b,
                                    question.choice_c, question.choice_d, question.answer))
                xz_question_list.append(xz_question)
            elif question.question_type == 'jd':
                jd_question = []
                jd_question.extend((question.id, question.context, question.answer))
                jd_question_list.append(jd_question)
        return render(request, 'homework_modification.html', locals())

    def post(self, request):
        homework_id = request.POST.get('homework-id')
        questions = Questions.objects.filter(homework_id=homework_id)
        for key in request.POST:
            if key.isdigit():
                question = questions.filter(id=key)
                if question.first().question_type == 'pd':
                    q = question.first()
                    if request.POST.get(key) != q.context or request.POST.get('answer' + key) != q.answer:
                        question.update(id=key, context=request.POST.get(key), answer=request.POST.get('answer' + key))
                elif question.first().question_type == 'xz':
                    q = question.first()
                    if request.POST.get(key) != q.context or request.POST.get(
                            'question' + key + "1") != q.choice_a or request.POST.get(
                        'question' + key + "2") != q.choice_a or request.POST.get(
                        'question' + key + "3") != q.choice_a or request.POST.get(
                        'question' + key + "4") != q.choice_a or request.POST.get('answer' + key) != q.answer:
                        question.update(id=key, context=request.POST.get(key), choice_a=request.POST.get(
                            'question' + key + "1"), choice_b=request.POST.get(
                            'question' + key + "2"), choice_c=request.POST.get(
                            'question' + key + "3"), choice_d=request.POST.get(
                            'question' + key + "4"), answer=request.POST.get('answer' + key))
                elif question.first().question_type == 'jd':
                    q = question.first()
                    if request.POST.get(key) != q.context or request.POST.get('answer' + key) != q.answer:
                        question.update(id=key, context=request.POST.get(key), answer=request.POST.get('answer' + key))
        return redirect(reverse('mine:mine'))


# 删除问题
class DeleteQuestion(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            homework_id = request.POST.get('homework-id')
            question_id = request.POST.get("question-id")
            question_delete_obj = Questions.objects.filter(homework_id=homework_id, id=question_id).delete()
            print(question_delete_obj)
            if question_delete_obj[1]:
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error"})
        except Exception as e:
            print('DeleteQuestion error:', e)
            return JsonResponse({"status": "error"})


# 删除作业
class DeleteHomework(View):

    def get(self, request):
        pass

    def post(self, request):
        try:
            homework_id = request.POST.get('homework-id')
            homework_delete_obj = Homework.objects.filter(id=homework_id).delete()
            if homework_delete_obj[1]:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error'})
        except Exception as e:
            print('DeleteHomework error:', e)
            return JsonResponse({'status': 'error'})
