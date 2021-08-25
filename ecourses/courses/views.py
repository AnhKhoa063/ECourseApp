from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from .serializers import CourseSerializer, LessonSerializer, UserSerializer, CategorySerializer
from .models import Course, Lesson, User, Category


# create your views here


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return [permissions.IsAuthenticated()]
    #
    #     return [permissions.AllowAny()]

    def get_permissions(self):
        if self.action == 'current-user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        return Response(self.serializer_class(request.user).data)


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # pagination_class = None



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    # permission_classes = [permissions.IsAuthenticated]
    swagger_schema = None

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]
    #     else:
    #         return [permissions.IsAuthenticated()]

    # list (get)  -> xem danh sach khoa hoc
    #     # .....(post) -> them khoa hoc
    #     # detail      -> xem chi tiet mot khoa hoc
    #     # update (put)-> cap nhat
    #     # delete      -> xoa khoa hoc


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description='This is a API that use to hide a lesson',
        responses={
            status.HTTP_200_OK: LessonSerializer()
        }
    )

    # hide lesson
    @action(methods=['post'], detail=True, url_path="hide-lesson", url_name="hide-lesson")
    def hide_lesson(self, request, pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data=LessonSerializer(l, context={'request': request}).data, status=status.HTTP_200_OK)


# Create your views here.
def index(request):
    return render(request, template_name='index.html', context={'name': 'Văn Trung'})


def welcome(request, year):
    return HttpResponse('Welcome ' + str(year))


class TestView(View):
    def get(self, request):
        return HttpResponse('Test class view')

    def post(self, request):
        pass
