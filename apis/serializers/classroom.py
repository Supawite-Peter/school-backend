from django.db import IntegrityError
from rest_framework import serializers
from apis.models import Classroom
from .simple import (
    SimpleSchoolSerializer,
    SimpleStudentSerializer,
    SimpleTeacherSerializer,
)


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            "id",
            "grade",
            "room",
            "school",
            "school_id",
            "teachers",
            "students",
        ]

    school = SimpleSchoolSerializer(read_only=True)
    school_id = serializers.ModelField(
        model_field=Classroom._meta.get_field("school"), write_only=True
    )
    teachers = SimpleTeacherSerializer(many=True, read_only=True)
    students = SimpleStudentSerializer(many=True, read_only=True)


class CreateClassroomSerializer(serializers.ModelSerializer):
    school_id = serializers.ModelField(model_field=Classroom._meta.get_field("school"))

    class Meta:
        model = Classroom
        fields = [
            "id",
            "grade",
            "room",
            "school_id",
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            throw_unique_error(
                self.Meta.fields,
                e,
                "Cannot create classroom with same grade and room in the same school",
            )


class UpdateClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            "grade",
            "room",
        ]

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as e:
            throw_unique_error(
                self.Meta.fields,
                e,
                "Cannot update classroom with same grade and room in the same school",
            )


def throw_unique_error(fields: list[str], error: IntegrityError, message: str):
    error_string = str(error)
    if "UNIQUE constraint" in error_string:
        error_output = {}
        for field in fields:
            if field in error_string and field != "id":
                error_output[field] = [message]
        raise serializers.ValidationError(error_output)
    raise IntegrityError
