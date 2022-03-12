"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from students.router import router as students_router

from rest_framework_bulk.routes import BulkRouter



router = BulkRouter()
router.registry.extend(students_router.registry)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^v1/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # re_path(r'^docs/', include_docs_urls("开源运维平台"))
]

