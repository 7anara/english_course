import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

LEVEL_CHOICES = (
    ('A1', 'A1'),
    ('A2', 'A2'),
    ('B1', 'B1'),
    ('B2', 'B2'),
    ('C1', 'C1'),
)

STATUS_CHOICES = (
    ('pending', 'Ожидает'),
    ('active', 'Активный'),
    ('expelled', 'Отчислен'),
)

class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=45)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Group(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teacher_groups')
    group_name = models.CharField(max_length=45)
    group_image = models.ImageField(upload_to='group_image/', null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='A1')
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.group_name} - {self.level}'


class Student(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} - {self.email}'


class Material(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='materials/', null=True, blank=True)

    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='materials')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.group.group_name}'


class Homework(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='homework/', null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_homeworks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.group.group_name}'


class HomeworkAnswer(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='answers')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homework_answers')
    file = models.FileField(upload_to='homework_answers/', null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('homework', 'student')

    def __str__(self):
        return f'{self.student.full_name} → {self.homework.title}'


class CourseTest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_tests')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.group.group_name}'


class TestQuestion(models.Model):
    test = models.ForeignKey(CourseTest, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    points = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.test.title} - {self.text[:50]}'


class TestAnswer(models.Model):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{"✓" if self.is_correct else "✗"} {self.text}'


class StudentTestResult(models.Model):
    test = models.ForeignKey(CourseTest, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='test_results')
    score = models.PositiveSmallIntegerField(default=0)
    max_score = models.PositiveSmallIntegerField(default=0)
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('test', 'student')

    def percentage(self):
        if self.max_score == 0:
            return 0
        return round((self.score / self.max_score) * 100)

    def __str__(self):
        return f'{self.student.full_name} - {self.score}/{self.max_score}'


class Rating(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='ratings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='ratings')
    rank = models.PositiveSmallIntegerField()
    note = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings_given')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']
        unique_together = ('group', 'student')

    def __str__(self):
        return f'#{self.rank} {self.student.full_name} - {self.group.group_name}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)],null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating}'