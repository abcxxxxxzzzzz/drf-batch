from .models import Classroom, Student, StudentImportFile
from rest_framework.serializers import ModelSerializer



# class StudentSerializer(ModelSerializer):

#     # 序列化添加数据
#     def to_representation(self, instance):
#         classroom = instance.classroom
#         ret =  super(StudentSerializer, self).to_representation(instance)
#         ret['classroom'] = {
#             "id": classroom.id,
#             "location": classroom.location
#         }
#         return ret


#     class Meta:
#         model = Student
#         fields = "__all__"


class ClassroomSerializer(ModelSerializer):
    # 序列化添加数据
    def to_representation(self, instance):
        ret = super(ClassroomSerializer, self).to_representation(instance)
        ret['count'] = instance.classrooms.all().count()
        return ret

    class Meta:
        model = Classroom
        fields = "__all__"

class StudentImportFileSerializer(ModelSerializer):
    class Meta:
        model = StudentImportFile
        fields = "__all__"

# ================================== 批量操作
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
)


class StudentSerializer(BulkSerializerMixin, ModelSerializer):
    
    # 序列化添加数据
    def to_representation(self, instance):
        classroom = instance.classroom
        ret =  super(StudentSerializer, self).to_representation(instance)
        ret['classroom'] = {
            "id": classroom.id,
            "location": classroom.location
        }
        return ret


    class Meta:
        model = Student
        fields = "__all__"
        list_serializer_class = BulkListSerializer