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
            self.throw_unique_error(e)

    def throw_unique_error(self, error):
        if "UNIQUE constraint" in str(error):
            raise serializers.ValidationError(
                {
                    "message": "Cannot create classroom with same grade and room in the same school"
                }
            )
        raise IntegrityError


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
            self.throw_unique_error(e)

    def throw_unique_error(self, error):
        if "UNIQUE constraint" in str(error):
            raise serializers.ValidationError(
                {
                    "message": "Cannot update classroom with same grade and room in the same school"
                }
            )
        raise IntegrityError
