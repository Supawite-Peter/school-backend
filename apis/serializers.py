from django.db.models.aggregates import Count
from django.forms.models import model_to_dict
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import School, Classroom, Student, Teacher


class SchoolSerializer(serializers.ModelSerializer):
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

    classrooms_count = serializers.SerializerMethodField(
        method_name="get_classrooms_count"
    )
    students_count = serializers.SerializerMethodField(method_name="get_students_count")
    teachers_count = serializers.SerializerMethodField(method_name="get_teachers_count")

    def get_classrooms_count(self, school: School):
        return school.classrooms.count()

    def get_students_count(self, school: School):
        return school.classrooms.aggregate(Count("students"))["students__count"]

    def get_teachers_count(self, school: School):
        return school.teachers.count()


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = [
            "id",
            "grade",
            "room",
            "school_detail",
            "school_id",
            "teachers",
            "students",
        ]

    school_detail = serializers.SerializerMethodField(
        method_name="get_school_detail", read_only=True
    )
    school_id = serializers.ModelField(
        model_field=Classroom._meta.get_field("school"), write_only=True
    )
    teachers = serializers.SerializerMethodField(
        method_name="get_teachers_list", read_only=True
    )
    students = serializers.SerializerMethodField(
        method_name="get_students_list", read_only=True
    )

    def get_teachers_list(self, classroom: Classroom):
        return [
            model_to_dict(teacher, fields=["id", "first_name", "last_name", "gender"])
            for teacher in classroom.teachers.all()
        ]

    def get_students_list(self, classroom: Classroom):
        return [
            model_to_dict(student, fields=["id", "first_name", "last_name", "gender"])
            for student in classroom.students.all()
        ]

    def get_school_detail(self, classroom: Classroom):
        return model_to_dict(classroom.school)

    def update(self, instance, validated_data):
        # Classroom should not be able to update school
        if "school_id" in validated_data:
            if validated_data["school_id"] != instance.school_id:
                raise serializers.ValidationError(
                    {"message": "Classroom should not be able to update school"}
                )
        try:
            return super().update(instance, validated_data)
        except IntegrityError as e:
            self.throw_unique_error(e)

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


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "school_id",
            "school_detail",
            "classrooms_id",
            "classrooms",
        ]

    school_detail = serializers.SerializerMethodField(
        method_name="get_school_detail", read_only=True
    )
    school_id = serializers.ModelField(
        model_field=Teacher._meta.get_field("school"), write_only=True
    )
    classrooms_id = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(), many=True, write_only=True
    )
    classrooms = serializers.SerializerMethodField(
        method_name="get_classrooms_list", read_only=True
    )

    def get_classrooms_list(self, teacher: Teacher):
        return [
            model_to_dict(classroom, fields=["id", "grade", "room"])
            for classroom in teacher.classrooms.all()
        ]

    def get_school_detail(self, teacher: Teacher):
        return model_to_dict(teacher.school)

    def create(self, validated_data):
        # Get classroom
        classrooms = validated_data.pop("classrooms_id")
        # Create new teacher first
        created_teacher = Teacher.objects.create(**validated_data)
        # Then add classrooms
        try:
            created_teacher.classrooms.add(*classrooms)
        except ValidationError as e:
            raise serializers.ValidationError({"classrooms_id": e})
        return created_teacher

    def update(self, instance, validated_data):
        with transaction.atomic():
            # Get classroom
            classrooms_data = validated_data.pop("classrooms_id")
            classrooms = instance.classrooms
            # Save first_name, last_name, gender first
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.last_name)
            instance.gender = validated_data.get("gender", instance.gender)
            instance.save()
            # Then update classrooms
            try:
                classrooms.set(classrooms_data)
            except ValidationError as e:
                raise serializers.ValidationError({"classrooms_id": e})

            return instance


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "school_detail",
            "classroom_id",
            "classroom_detail",
        ]

    school_detail = serializers.SerializerMethodField(
        method_name="get_school_detail", read_only=True
    )
    classroom_id = serializers.ModelField(
        model_field=Student._meta.get_field("classroom"), write_only=True
    )
    classroom_detail = serializers.SerializerMethodField(
        method_name="get_classroom_detail", read_only=True
    )

    def get_school_detail(self, student: Student):
        return model_to_dict(student.classroom.school)

    def get_classroom_detail(self, student: Student):
        return model_to_dict(student.classroom, fields=["id", "grade", "room"])
