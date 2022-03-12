
# Create your views here.


from rest_framework.viewsets import ModelViewSet
from .serializers import StudentSerializer, ClassroomSerializer, StudentImportFileSerializer
from .models import Student, Classroom, StudentImportFile
from rest_framework.permissions import IsAuthenticated, AllowAny


# class StudentViewSet(ModelViewSet):
#     serializer_class = StudentSerializer
#     queryset = Student.objects.all()



class ClassroomViewSet(ModelViewSet):
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()
    permission_classes = [IsAuthenticated,]



from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin

# 只允许上传，查看
class StudentImportFileViewSet(GenericViewSet,ListModelMixin,CreateModelMixin,RetrieveModelMixin):
# class StudentImportFileViewSet(ModelViewSet):
    serializer_class = StudentImportFileSerializer
    queryset = StudentImportFile.objects.all()
    permission_classes = [IsAuthenticated,]

    


# ========================== 批量操作
from rest_framework_bulk import BulkModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filter import StudentFilter,StudentSearch
from .pagination import LargeResultsSetPagination
from .models import Student
from rest_framework.decorators import action
import time
from djqscsv import render_to_csv_response

from .models import StudentImportFile
from .permissions import Permissions

class StudentViewSet(BulkModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [Permissions,]

    # 模糊查询单个 name 字段, 和批量查询 name 绝对值
    filter_backends = [DjangoFilterBackend,OrderingFilter,StudentSearch]
    filter_class = StudentFilter
    search_fields = ['=name']
    ordering_fields = ['id']
    # filterset_fields = ['name', 'classroom']
    # filter_backends = [DjangoFilterBackend,SearchFilter]
    pagination_class = LargeResultsSetPagination



    
    # 重写 allow_bulk_destroy
    def allow_bulk_destroy(self, qs, filtered):
        # 业务逻辑；（设置不允许全部删除,结合批量搜索和过滤器，判断是否有值,如果没有的话，返回False,如果有则执行删除)
        name = self.request.query_params.get('name',default=None)
        classroom = self.request.query_params.get('classroom',default=None)
        search = self.request.query_params.get('search',default=None)
        if name or classroom or search:
            return True
        return False
        

        # qs参数是一个查询集，它来自self.get_queryset()
        # 默认要检查qs是否被过滤了。
        # filtered 参数来自self.filter_queryset(qs)
        # return qs is not filtered   # 最终返回True，则执行删除操作。返回False，则不执行。

    @action(detail=False, methods=["get"])
    def download(self, request):
        '''参考： https://pypi.org/project/django-queryset-csv/'''
        # 默认下载数据库中所有数据
        qs = self.get_queryset()
        filtered = self.filter_queryset(qs)
        print(qs)
        print(filtered)
        filename = time.strftime("%Y%m%d%H%M%S", time.localtime())
        qs = Student.objects.values('id','name', 'classroom__location')

        # 由于使用外键导出数据，无法获得指定的 verbose_names,这里自定义赋值一下
        field_header_map = {'classroom__location': '所属班级'}
        return render_to_csv_response(qs,filename=filename, field_header_map=field_header_map)


