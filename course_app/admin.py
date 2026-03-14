from django.contrib import admin
from .models import (
    UserProfile, Group, Student, Material,
    Homework, HomeworkAnswer, CourseTest,
    TestQuestion, TestAnswer, StudentTestResult,
    Rating, Review
)


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1

class StudentInline(admin.TabularInline):
    model = Student
    extra = 1

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1

class HomeworkInline(admin.TabularInline):
    model = Homework
    extra = 1

class HomeworkAnswerInline(admin.TabularInline):
    model = HomeworkAnswer
    extra = 1

class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 1

class TestAnswerInline(admin.TabularInline):
    model = TestAnswer
    extra = 1

class StudentTestResultInline(admin.TabularInline):
    model = StudentTestResult
    extra = 1

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1



class UserProfileAdmin(admin.ModelAdmin):
    inlines = [GroupInline]

class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline, MaterialInline, HomeworkInline, RatingInline]

class StudentAdmin(admin.ModelAdmin):
    inlines = [HomeworkAnswerInline]

class HomeworkAdmin(admin.ModelAdmin):
    inlines = [HomeworkAnswerInline, ReviewInline]

class CourseTestAdmin(admin.ModelAdmin):
    inlines = [TestQuestionInline, StudentTestResultInline]

class TestQuestionAdmin(admin.ModelAdmin):
    inlines = [TestAnswerInline]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Material)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(HomeworkAnswer)
admin.site.register(CourseTest, CourseTestAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(TestAnswer)
admin.site.register(StudentTestResult)
admin.site.register(Rating)
admin.site.register(Review)