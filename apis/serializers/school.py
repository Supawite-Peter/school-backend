from django.db.models.aggregates import Count
from rest_framework import serializers
from apis.models import School


class SchoolSerializer(serializers.ModelSerializer):
    classrooms_count = serializers.SerializerMethodField(
        method_name="get_classrooms_count"
    )
    students_count = serializers.SerializerMethodField(method_name="get_students_count")
    teachers_count = serializers.SerializerMethodField(method_name="get_teachers_count")

    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "alias",
            "address",
            "classrooms_count",
            "students_count",
            "teachers_count",
        ]

    def get_classrooms_count(self, school: School):
        return school.classrooms.count()

    def get_students_count(self, school: School):
        return school.classrooms.aggregate(Count("students"))["students__count"]

    def get_teachers_count(self, school: School):
        return school.teachers.count()


class CreateUpdateSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            "id",
            "name",
            "alias",
            "address",
        ]
