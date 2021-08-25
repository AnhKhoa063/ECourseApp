from django.urls import path, re_path, include
from . import views
from .admin import admin_site
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('courses', views.CourseViewSet)
router.register('lessons', views.LessonViewSet)
router.register('users', views.UserViewSet)
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include((router.urls))),
    path('', views.index, name="index"),
    re_path(r'^welcome/(?P<year>[0-9]{3,4})/$', views.welcome, name='welcome'),
    path('testing/', views.TestView.as_view(), name='testing'),
    path('admin/', admin_site.urls),
]