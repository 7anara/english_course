from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import (
    UserProfile, Group, Student, Material,
    Homework, HomeworkAnswer, CourseTest,
    TestQuestion, TestAnswer, StudentTestResult,
    Rating, Review
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number',]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")
    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'full_name', 'email',
                  'avatar', 'phone_number', 'bio', 'register_date']
        read_only_fields = ['register_date']



class GroupListSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_image',
                  'level', 'invite_code', 'created_date', 'students_count']
        read_only_fields = ['invite_code', 'created_date']

    def get_students_count(self, obj):
        return obj.students.filter(status='active').count()


class GroupDetailSerializer(serializers.ModelSerializer):
    students_count = serializers.SerializerMethodField()
    materials_count = serializers.SerializerMethodField()
    homeworks_count = serializers.SerializerMethodField()
    tests_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_image', 'level',
                  'invite_code', 'created_date', 'students_count',
                  'materials_count', 'homeworks_count', 'tests_count']
        read_only_fields = ['invite_code', 'created_date']

    def get_students_count(self, obj):
        return obj.students.filter(status='active').count()

    def get_materials_count(self, obj):
        return obj.materials.count()

    def get_homeworks_count(self, obj):
        return obj.homeworks.count()

    def get_tests_count(self, obj):
        return obj.tests.count()


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_image', 'level']



class StudentJoinSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()


class StudentListSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.group_name', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'email',
                  'group', 'group_name', 'status', 'joined_at']
        read_only_fields = ['joined_at']


class StudentDetailSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    group_level = serializers.CharField(source='group.level', read_only=True)
    rating = serializers.SerializerMethodField()
    homework_answers_count = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'email', 'group', 'group_name',
                  'group_level', 'status', 'joined_at',
                  'rating', 'homework_answers_count']
        read_only_fields = ['joined_at']

    def get_rating(self, obj):
        rating = obj.ratings.first()
        if rating:
            return {'rank': rating.rank, 'note': rating.note}
        return None

    def get_homework_answers_count(self, obj):
        return obj.homework_answers.count()


class StudentAddToGroupSerializer(serializers.Serializer):
    group_id = serializers.IntegerField()



class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'group', 'title', 'created_at']
        read_only_fields = ['created_at']


class MaterialDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'group', 'title', 'description', 'file', 'created_at']
        read_only_fields = ['created_at']

class HomeworkAnswerSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = HomeworkAnswer
        fields = ['id', 'homework', 'student', 'student_name',
                  'file', 'comment', 'submitted_at']
        read_only_fields = ['submitted_at']


class HomeworkListSerializer(serializers.ModelSerializer):
    answers_count = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ['id', 'group', 'title', 'due_date',
                  'created_at', 'answers_count']
        read_only_fields = ['created_at']

    def get_answers_count(self, obj):
        return obj.answers.count()


class HomeworkDetailSerializer(serializers.ModelSerializer):
    answers_count = serializers.SerializerMethodField()
    answers = HomeworkAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Homework
        fields = ['id', 'group', 'title', 'description', 'file',
                  'due_date', 'created_at', 'answers_count', 'answers']
        read_only_fields = ['created_at']

    def get_answers_count(self, obj):
        return obj.answers.count()


class HomeworkStudentSerializer(serializers.ModelSerializer):
    is_submitted = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ['id', 'title', 'description',
                  'file', 'due_date', 'created_at', 'is_submitted']
        read_only_fields = ['created_at']

    def get_is_submitted(self, obj):
        student_email = self.context.get('student_email')
        if student_email:
            return obj.answers.filter(student__email=student_email).exists()
        return False



class TestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAnswer
        fields = ['id', 'text', 'is_correct']


class TestAnswerStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAnswer
        fields = ['id', 'text']


class TestQuestionSerializer(serializers.ModelSerializer):
    answers = TestAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = TestQuestion
        fields = ['id', 'text', 'points', 'answers']


class TestQuestionStudentSerializer(serializers.ModelSerializer):
    answers = TestAnswerStudentSerializer(many=True, read_only=True)

    class Meta:
        model = TestQuestion
        fields = ['id', 'text', 'points', 'answers']


class CourseTestListSerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = CourseTest
        fields = ['id', 'group', 'title', 'created_at', 'questions_count']
        read_only_fields = ['created_at']

    def get_questions_count(self, obj):
        return obj.questions.count()


class CourseTestDetailSerializer(serializers.ModelSerializer):
    questions = TestQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = CourseTest
        fields = ['id', 'group', 'title', 'description',
                  'created_at', 'questions']
        read_only_fields = ['created_at']


class CourseTestStudentSerializer(serializers.ModelSerializer):
    questions = TestQuestionStudentSerializer(many=True, read_only=True)

    class Meta:
        model = CourseTest
        fields = ['id', 'title', 'description', 'created_at', 'questions']
        read_only_fields = ['created_at']


class StudentTestResultSerializer(serializers.ModelSerializer):
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = StudentTestResult
        fields = ['id', 'test', 'student', 'score',
                  'max_score', 'percentage', 'taken_at']
        read_only_fields = ['taken_at']

    def get_percentage(self, obj):
        return obj.percentage()



class RatingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'group', 'student', 'student_name',
                  'rank', 'note', 'created_at']
        read_only_fields = ['created_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'homework', 'text', 'rating', 'created_date']
        read_only_fields = ['created_date']


