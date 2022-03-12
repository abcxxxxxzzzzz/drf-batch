from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ClassroomViewSet, StudentImportFileViewSet

from rest_framework_bulk.routes import BulkRouter


# router = DefaultRouter()
router = BulkRouter()
router.register(r'students', StudentViewSet, basename='students')
router.register(r'file', StudentImportFileViewSet, basename='students_upload')
router.register(r'classroom', ClassroomViewSet, basename='classroom')



