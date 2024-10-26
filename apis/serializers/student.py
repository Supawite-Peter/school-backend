from rest_framework import serializers
from apis.models import Student
from .simple import SimpleSchoolSerializer, SimpleClassroomSerializer


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "school",
            "classroom",
        ]

    school = SimpleSchoolSerializer(source="classroom.school", read_only=True)
    classroom = SimpleClassroomSerializer(read_only=True)


class CreateStudentSerializer(StudentSerializer):
    classroom_id = serializers.ModelField(
        model_field=Student._meta.get_field("classroom")
    )

    class Meta(StudentSerializer.Meta):
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "classroom_id",
        ]


class UpdateStudentSerializer(CreateStudentSerializer):
    class Meta(CreateStudentSerializer.Meta):
        fields = [
            "first_name",
            "last_name",
            "gender",
            "classroom_id",
        ]
