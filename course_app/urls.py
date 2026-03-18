from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, LogoutView, RegisterView, UserProfileDetailAPIView,
    GroupListAPIView, GroupDetailAPIView, GroupViewSet, GroupStudentListAPIView,
    StudentDetailAPIView, JoinGroupView,
    MaterialListAPIView, MaterialDetailAPIView, MaterialViewSet, StudentMaterialListAPIView,
    HomeworkListAPIView, HomeworkDetailAPIView, HomeworkViewSet, StudentHomeworkListAPIView,
    HomeworkAnswerCreateAPIView, HomeworkAnswerListAPIView,
    CourseTestListAPIView, CourseTestDetailAPIView, CourseTestViewSet,
    TestQuestionViewSet, TestAnswerViewSet, StudentTestDetailAPIView, TestResultListAPIView,
    RatingListAPIView, RatingViewSet,
    ReviewCreateAPIView, ReviewEditAPIView
)

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'homeworks', HomeworkViewSet, basename='homework')
router.register(r'coursetests', CourseTestViewSet, basename='coursetest')
router.register(r'testquestions', TestQuestionViewSet, basename='testquestion')
router.register(r'testanswers', TestAnswerViewSet, basename='testanswer')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),

    path('register', RegisterView.as_view(), name='registrations'),
    path('login', LoginView.as_view(), name = 'login'),
    path('logout', LogoutView.as_view(), name = 'logout'),

    path('users/me/', UserProfileDetailAPIView.as_view(), name='user-detail'),
    path('groups/<int:group_id>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/students/', GroupStudentListAPIView.as_view(), name='group-students'),
    path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
    path('join/<uuid:invite_code>/', JoinGroupView.as_view(), name='join-group'),
    path('groups/<int:group_id>/materials/', MaterialListAPIView.as_view(), name='material-list'),
    path('materials/<int:pk>/', MaterialDetailAPIView.as_view(), name='material-detail'),
    path('students/materials/', StudentMaterialListAPIView.as_view(), name='student-materials'),
    path('groups/<int:group_id>/homeworks/', HomeworkListAPIView.as_view(), name='homework-list'),
    path('homeworks/<int:pk>/', HomeworkDetailAPIView.as_view(), name='homework-detail'),
    path('students/homeworks/', StudentHomeworkListAPIView.as_view(), name='student-homeworks'),
    path('homeworks/<int:homework_id>/answers/', HomeworkAnswerCreateAPIView.as_view(), name='homework-answer-create'),
    path('homeworks/<int:homework_id>/answers/list/', HomeworkAnswerListAPIView.as_view(), name='homework-answer-list'),
    path('groups/<int:group_id>/tests/', CourseTestListAPIView.as_view(), name='coursetest-list'),
    path('tests/<int:pk>/', CourseTestDetailAPIView.as_view(), name='coursetest-detail'),
    path('students/tests/<int:test_id>/', StudentTestDetailAPIView.as_view(), name='student-test-detail'),
    path('tests/<int:test_id>/results/', TestResultListAPIView.as_view(), name='test-result-list'),
    path('groups/<int:group_id>/ratings/', RatingListAPIView.as_view(), name='rating-list'),
    path('homeworks/<int:homework_id>/reviews/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', ReviewEditAPIView.as_view(), name='review-edit'),
]