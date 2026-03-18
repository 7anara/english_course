from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .permission import IsTeacherPermission, IsOwnerPermission


from .models import (UserProfile, Group, Student, Material,
                     Homework, HomeworkAnswer, CourseTest, TestQuestion,
                     TestAnswer, StudentTestResult, Rating, Review)
from .serializers import (
    LoginSerializer, UserProfileSerializer, LogoutSerializer,
    GroupListSerializer, GroupDetailSerializer, GroupCreateUpdateSerializer,
    StudentJoinSerializer, StudentListSerializer, StudentDetailSerializer,
    MaterialListSerializer, MaterialDetailSerializer,
    HomeworkListSerializer, HomeworkDetailSerializer, HomeworkStudentSerializer,
    HomeworkAnswerSerializer,
    TestQuestionSerializer, TestAnswerSerializer,
    CourseTestListSerializer, CourseTestDetailSerializer, CourseTestStudentSerializer,
    StudentTestResultSerializer,
    RatingSerializer, ReviewSerializer, UserSerializer
)
from .filters import GroupFilter, StudentFilter, HomeworkFilter, CourseTestFilter
from .pagination import StandardPagination
#from .permissions import IsTeacherPermission, IsOwnerPermission

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GroupFilter
    search_fields = ['group_name']
    ordering_fields = ['created_date', 'level']
    ordering = ['-created_date']
    pagination_class = StandardPagination

    def get_queryset(self):
        return Group.objects.filter(teacher=self.request.user)


class GroupDetailAPIView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(teacher=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    def get_queryset(self):
        return Group.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class GroupStudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = StudentFilter
    search_fields = ['full_name', 'email']
    ordering_fields = ['full_name', 'joined_at']
    ordering = ['full_name']
    pagination_class = StandardPagination

    def get_queryset(self):
        return Student.objects.filter(
            group_id=self.kwargs['group_id'],
            group__teacher=self.request.user
        )


class StudentDetailAPIView(generics.RetrieveAPIView):

    queryset = Student.objects.all()
    serializer_class = StudentDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(group__teacher=self.request.user)


class JoinGroupView(generics.CreateAPIView):

    serializer_class = StudentJoinSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        try:
            group = Group.objects.get(invite_code=self.kwargs['invite_code'])
        except Group.DoesNotExist:
            return Response({'detail': 'Чакыруу коду табылган жок.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        full_name = serializer.validated_data['full_name']

        student, created = Student.objects.get_or_create(
            email=email,
            defaults={'full_name': full_name, 'group': group, 'status': 'pending'}
        )
        if not created:
            if student.group == group:
                return Response({'detail': 'Бул email менен студент мурунтан кошулган.'}, status=status.HTTP_400_BAD_REQUEST)
            student.group = group
            student.status = 'pending'
            student.save()

        return Response(
            StudentListSerializer(student).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class MaterialListAPIView(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    pagination_class = StandardPagination

    def get_queryset(self):
        return Material.objects.filter(
            group_id=self.kwargs['group_id'],
            group__teacher=self.request.user
        )


class MaterialDetailAPIView(generics.RetrieveAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Material.objects.filter(group__teacher=self.request.user)


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]


    def get_queryset(self):
        return Material.objects.filter(group__teacher=self.request.user)

    def perform_create(self, serializer):
        group = Group.objects.get(id=self.request.data.get('group'), teacher=self.request.user)
        serializer.save(created_by=self.request.user, group=group)


class StudentMaterialListAPIView(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    pagination_class = StandardPagination

    def get_queryset(self):
        email = self.request.query_params.get('email')
        group_id = self.request.query_params.get('group_id')
        if not email or not group_id:
            return Material.objects.none()
        try:
            Student.objects.get(email=email, group_id=group_id, status='active')
        except Student.DoesNotExist:
            return Material.objects.none()
        return Material.objects.filter(group_id=group_id)

class HomeworkListAPIView(generics.ListAPIView):

    queryset = Homework.objects.all()
    serializer_class = HomeworkListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = HomeworkFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['-created_at']
    pagination_class = StandardPagination

    def get_queryset(self):
        return Homework.objects.filter(
            group_id=self.kwargs['group_id'],
            group__teacher=self.request.user
        )


class HomeworkDetailAPIView(generics.RetrieveAPIView):

    queryset = Homework.objects.all()
    serializer_class = HomeworkDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Homework.objects.filter(group__teacher=self.request.user)


class HomeworkViewSet(viewsets.ModelViewSet):

    queryset = Homework.objects.all()
    serializer_class = HomeworkDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    def get_queryset(self):
        return Homework.objects.filter(group__teacher=self.request.user)

    def perform_create(self, serializer):
        group = Group.objects.get(id=self.request.data.get('group'), teacher=self.request.user)
        serializer.save(created_by=self.request.user, group=group)


class StudentHomeworkListAPIView(generics.ListAPIView):
    queryset = Homework.objects.all()
    serializer_class = HomeworkStudentSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['-created_at']
    pagination_class = StandardPagination

    def get_queryset(self):
        email = self.request.query_params.get('email')
        group_id = self.request.query_params.get('group_id')
        if not email or not group_id:
            return Homework.objects.none()
        try:
            Student.objects.get(email=email, group_id=group_id, status='active')
        except Student.DoesNotExist:
            return Homework.objects.none()
        return Homework.objects.filter(group_id=group_id)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['student_email'] = self.request.query_params.get('email')
        return ctx

class HomeworkAnswerCreateAPIView(generics.CreateAPIView):

    queryset = HomeworkAnswer.objects.all()
    serializer_class = HomeworkAnswerSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        try:
            homework = Homework.objects.get(id=self.kwargs['homework_id'])
        except Homework.DoesNotExist:
            return Response({'detail': 'Тапшырма табылган жок.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            student = Student.objects.get(
                id=request.data.get('student_id'),
                group=homework.group,
                status='active'
            )
        except Student.DoesNotExist:
            return Response({'detail': 'Студент табылган жок же активдүү эмес.'}, status=status.HTTP_404_NOT_FOUND)

        answer, created = HomeworkAnswer.objects.get_or_create(
            homework=homework,
            student=student,
            defaults={
                'file': request.FILES.get('file'),
                'comment': request.data.get('comment', '')
            }
        )
        if not created:
            answer.file = request.FILES.get('file', answer.file)
            answer.comment = request.data.get('comment', answer.comment)
            answer.save()

        return Response(
            HomeworkAnswerSerializer(answer).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class HomeworkAnswerListAPIView(generics.ListAPIView):
    queryset = HomeworkAnswer.objects.all()
    serializer_class = HomeworkAnswerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['student__full_name', 'student__email']
    ordering_fields = ['submitted_at']
    ordering = ['-submitted_at']
    pagination_class = StandardPagination

    def get_queryset(self):
        return HomeworkAnswer.objects.filter(
            homework_id=self.kwargs['homework_id'],
            homework__group__teacher=self.request.user
        )

class CourseTestListAPIView(generics.ListAPIView):

    queryset = CourseTest.objects.all()
    serializer_class = CourseTestListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseTestFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    pagination_class = StandardPagination

    def get_queryset(self):
        return CourseTest.objects.filter(
            group_id=self.kwargs['group_id'],
            group__teacher=self.request.user
        )


class CourseTestDetailAPIView(generics.RetrieveAPIView):

    queryset = CourseTest.objects.all()
    serializer_class = CourseTestDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CourseTest.objects.filter(group__teacher=self.request.user)


class CourseTestViewSet(viewsets.ModelViewSet):
    queryset = CourseTest.objects.all()
    serializer_class = CourseTestDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission]

    def get_queryset(self):
        return CourseTest.objects.filter(group__teacher=self.request.user)

    def perform_create(self, serializer):
        group = Group.objects.get(id=self.request.data.get('group'), teacher=self.request.user)
        serializer.save(created_by=self.request.user, group=group)

class TestQuestionViewSet(viewsets.ModelViewSet):

    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['text']
    ordering_fields = ['points']

    def get_queryset(self):
        return TestQuestion.objects.filter(
            test_id=self.kwargs['test_id'],
            test__group__teacher=self.request.user
        )

    def perform_create(self, serializer):
        test = CourseTest.objects.get(id=self.kwargs['test_id'], group__teacher=self.request.user)
        serializer.save(test=test)


class TestAnswerViewSet(viewsets.ModelViewSet):

    queryset = TestAnswer.objects.all()
    serializer_class = TestAnswerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_correct']
    search_fields = ['text']

    def get_queryset(self):
        return TestAnswer.objects.filter(
            question_id=self.kwargs['question_id'],
            question__test__group__teacher=self.request.user
        )

    def perform_create(self, serializer):
        question = TestQuestion.objects.get(
            id=self.kwargs['question_id'],
            test__group__teacher=self.request.user
        )
        serializer.save(question=question)

class StudentTestDetailAPIView(generics.RetrieveAPIView):

    queryset = CourseTest.objects.all()
    serializer_class = CourseTestStudentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        test = generics.get_object_or_404(CourseTest, id=self.kwargs['test_id'])
        email = self.request.query_params.get('email')
        if email:
            generics.get_object_or_404(Student, email=email, group=test.group, status='active')
        return test


class TestResultListAPIView(generics.ListAPIView):
    queryset = StudentTestResult.objects.all()
    serializer_class = StudentTestResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['student__full_name', 'student__email']
    ordering_fields = ['score', 'taken_at']
    ordering = ['-score']
    pagination_class = StandardPagination

    def get_queryset(self):
        return StudentTestResult.objects.filter(
            test_id=self.kwargs['test_id'],
            test__group__teacher=self.request.user
        )

class RatingListAPIView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['student__full_name', 'note']
    ordering_fields = ['rank']
    ordering = ['rank']
    pagination_class = StandardPagination

    def get_queryset(self):
        return Rating.objects.filter(
            group_id=self.kwargs['group_id'],
            group__teacher=self.request.user
        )


class RatingViewSet(viewsets.ModelViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


    def get_queryset(self):
        return Rating.objects.filter(group__teacher=self.request.user)

    def perform_create(self, serializer):
        group = Group.objects.get(id=self.request.data.get('group'), teacher=self.request.user)
        serializer.save(created_by=self.request.user, group=group)

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        homework = Homework.objects.get(id=self.kwargs['homework_id'])
        serializer.save(user=self.request.user, homework=homework)


class ReviewEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)