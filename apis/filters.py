from django_filters import FilterSet, filters
from .models import School, Classroom, Student, Teacher


class SchoolFilter(FilterSet):
    class Meta:
        model = School
        fields = {
            "name": ["iexact", "icontains"],
        }


class ClassroomFilter(FilterSet):
    class Meta:
        model = Classroom
        fields = {
            "school": ["exact"],
        }


class StudentFilter(FilterSet):
    school = filters.ChoiceFilter(
        field_name="classroom__school",
        choices=School.objects.values_list("id", "name"),
    )

    class Meta:
        model = Student
        fields = {
            "classroom": ["exact"],
            "first_name": ["iexact", "icontains"],
            "last_name": ["iexact", "icontains"],
            "gender": ["iexact"],
        }


class TeacherFilter(FilterSet):
    class Meta:
        model = Teacher
        fields = {
            "school": ["exact"],
            "classrooms": ["exact"],
            "first_name": ["iexact", "icontains"],
            "last_name": ["iexact", "icontains"],
            "gender": ["iexact"],
        }
