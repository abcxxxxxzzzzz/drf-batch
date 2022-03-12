from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import os, csv
from django.conf import settings

# Create your models here.

class Classroom(models.Model):

    location = models.CharField(max_length=128, verbose_name='班级')
    def __str__(self):
        return self.location


class Student(models.Model):
    name = models.CharField(max_length=32, verbose_name='学生名字')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='classrooms', verbose_name='所属班级')

    def __str__(self):
        return self.name


class StudentImportFile(models.Model):
    # upload to MEDIA_ROOT/temp
    student_import = models.FileField(upload_to="temp",
                                      blank=False,
                                      null=False, verbose_name='上传文件', help_text='文件内学生名字不能已经存在数据库中,如果班级没有会自动创建')
    class Meta:
        ordering = ['-id']
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         old_import = StudentImportFile.objects.get(pk=self.pk)

    #         if old_import.student_import:
    #             old_import.student_import.delete(save=False)

    #     return super(StudentImportFile, self).save(*args, **kwargs)

# 创建上传文件后的信号机制
@receiver(post_save, sender=StudentImportFile, dispatch_uid="add_records_to_student_from_import_file")
def add_records_to_student_from_import_file(sender, instance, **kwargs):
    to_import = os.path.join(settings.MEDIA_ROOT, instance.student_import.name)
    with open(to_import, encoding='gb2312') as f:
        reader = csv.DictReader(f)
        try:
            temp_list = []
            temp_error = []
            temp_add_data = []
            for row in reader:
                content_name = row['学生名字'].replace(' ','')
                content_classroom = row['所属班级'].replace(' ','')
                # 为了减少数据库查询压力，判断是否在自定义的数组中, 判断是否有班级，没有班级就创建班级,添加到自定义数组中,创建失败添加到错误数组中
                if content_name not in temp_list:
                    classroom = Classroom.objects.get_or_create(location=content_classroom)
                    if not classroom:
                        temp_error.append(content_name)
                        continue
                    temp_list.append(content_name)
                # 组合数据，方便批量添加
                obj_classroom = Classroom.objects.get(location=content_classroom)
                temp_add_data.append(Student(name=content_name, classroom=obj_classroom))
    
                # print("="*30)
                # print(temp_add_data)
                # import time
                # time.sleep(10)
                # s = Student(name=name,classroom=classroom)
            insert_to = Student.objects.bulk_create(temp_add_data, ignore_conflicts=True)
            return insert_to
        except Exception as e:
            print(e)

            