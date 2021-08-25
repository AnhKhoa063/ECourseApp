from rest_framework.serializers import ModelSerializer
from .models import Course, Lesson, Tag, User, Category


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    # cach 2
    # def create(self, validated_data):
    #     #     user = User()
    #     #     user.first_name = validated_data('first_name')
    #     #     user.last_name = validated_data('last_name')
    #     #     user.set_password(validated_data['password'])


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "subject", "image", "create_date", "category", "image"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class LessonSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ["id", "subject", "content", "create_date", "course", "tags", "image"]
