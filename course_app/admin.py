from django.contrib import admin
from .models import *

class GroupInline(admin.TabularInline):
    model = Group
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [GroupInline]

class StudentAdmin(admin.ModelAdmin):
    inlines = [GroupInline]

class MaterialAdmin(admin.ModelAdmin):
    inlines = [GroupInline]

class HomeworkAdmin(admin.ModelAdmin):
    inlines = [GroupInline]

class CourseTestAdmin(admin.ModelAdmin):
    inlines = [GroupInline]

class HomeworkInline(admin.TabularInline):
    model = Homework
    extra = 1

class HomeworkAnswerAdmin(admin.ModelAdmin):
    inlines = [HomeworkInline]

class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 1

class CourseTestAdmin(admin.ModelAdmin):
    inlines = [TestQuestionInline]

class TestAnswerInline(admin.TabularInline):
    model = TestAnswer
    extra = 1

class TestQuestionAdmin(admin.ModelAdmin):
    inlines = [TestAnswerInline]

class StudentTestResultInline(admin.TabularInline):
    model = StudentTestResult
    extra = 1

class CourseTestAdmin(admin.ModelAdmin):
    inlines = [StudentTestResultInline]

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    inlines = [RatingInline]

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Material)
admin.site.register(Homework)
admin.site.register(HomeworkAnswer)
admin.site.register(CourseTest, CourseTestAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(TestAnswer)
admin.site.register(StudentTestResult)
admin.site.register(Rating)
admin.site.register(Review)