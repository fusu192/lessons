# Generated by Django 2.0.13 on 2019-04-05 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='作业名')),
                ('describe', models.CharField(blank=True, default='无', max_length=200, verbose_name='作业说明')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('answer_nums', models.CharField(default=0, editable=False, max_length=10, verbose_name='作答人数')),
                ('release', models.BooleanField(default=False, verbose_name='是否发布')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.Specialty', verbose_name='专业')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.TeacherProfile', verbose_name='老师')),
            ],
            options={
                'verbose_name': '作业',
                'verbose_name_plural': '作业',
                'db_table': 'homeworks',
                'ordering': ['-add_time'],
            },
        ),
        migrations.CreateModel(
            name='HomeworkSocre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pd_score', models.FloatField(blank=True, default=1, verbose_name='判断分值')),
                ('xz_score', models.FloatField(blank=True, default=1, verbose_name='选择分值')),
                ('jd_score', models.FloatField(blank=True, default=1, verbose_name='简答分值')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworkapp.Homework', verbose_name='作业名')),
            ],
            options={
                'verbose_name': '作业总分',
                'verbose_name_plural': '作业总分',
                'db_table': 'homework_socre',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('pd', '判断'), ('xz', '选择'), ('jd', '简答')], max_length=2, verbose_name='题目类型')),
                ('context', models.TextField(verbose_name='题目内容')),
                ('answer', models.TextField(verbose_name='正确答案')),
                ('choice_a', models.TextField(default='我是答案A', verbose_name='A选项')),
                ('choice_b', models.TextField(default='我是答案B', verbose_name='B选项')),
                ('choice_c', models.TextField(default='我是答案C', verbose_name='C选项')),
                ('choice_d', models.TextField(default='我是答案D', verbose_name='D选项')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworkapp.Homework', verbose_name='作业名')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.TeacherProfile', verbose_name='老师')),
            ],
            options={
                'verbose_name': '题目',
                'verbose_name_plural': '题目',
                'db_table': 'questions',
                'ordering': ['question_type'],
            },
        ),
        migrations.CreateModel(
            name='StudentAnswerLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(choices=[('pd', '判断'), ('xz', '选择'), ('jd', '简答')], max_length=2, verbose_name='题目类型')),
                ('answer', models.TextField(verbose_name='用户答案')),
                ('score', models.FloatField(default=0, max_length=100, verbose_name='分数')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='作答时间')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworkapp.Homework', verbose_name='作业名')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworkapp.Questions', verbose_name='题目')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.StudentProfile', verbose_name='学生')),
            ],
            options={
                'verbose_name': '做题记录',
                'verbose_name_plural': '做题记录',
                'db_table': 'student_answer_log',
            },
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pd_score', models.FloatField(default=0, verbose_name='判断')),
                ('xz_score', models.FloatField(default=0, verbose_name='选择')),
                ('jd_score', models.FloatField(default=0, verbose_name='简答')),
                ('total', models.FloatField(default=0, verbose_name='总分')),
                ('correct', models.BooleanField(default=False, verbose_name='是否批改')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='提交时间')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworkapp.Homework', verbose_name='作业名')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.StudentProfile', verbose_name='学生')),
            ],
            options={
                'verbose_name': '学生总分',
                'verbose_name_plural': '学生总分',
                'db_table': 'student_score',
            },
        ),
    ]
