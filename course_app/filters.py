import django_filters
from .models import Group, Student, Homework, CourseTest


class GroupFilter(django_filters.FilterSet):
    level = django_filters.ChoiceFilter(choices=[
        ('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1')
    ])

    class Meta:
        model = Group
        fields = ['level']


class StudentFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[
        ('pending', 'Ожидает'), ('active', 'Активный'), ('expelled', 'Отчислен')
    ])

    class Meta:
        model = Student
        fields = ['status']


class HomeworkFilter(django_filters.FilterSet):
    due_date_from = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    due_date_to   = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')

    class Meta:
        model = Homework
        fields = ['due_date_from', 'due_date_to']


class CourseTestFilter(django_filters.FilterSet):
    class Meta:
        model = CourseTest
        fields = ['group']