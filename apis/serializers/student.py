from rest_framework import serializers
from apis.models import Student, Classroom
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

    def validate_classroom_id(self, value):
        if not Classroom.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "No classroom with the given ID was found."
            )
        return value


class UpdateStudentSerializer(CreateStudentSerializer):
    class Meta(CreateStudentSerializer.Meta):
        fields = [
            "first_name",
            "last_name",
            "gender",
            "classroom_id",
        ]
