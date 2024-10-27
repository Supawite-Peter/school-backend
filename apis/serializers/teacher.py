from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers
from apis.models import Teacher, Classroom, School
from .simple import SimpleClassroomSerializer, SimpleSchoolSerializer


class TeacherSerializer(serializers.ModelSerializer):
    school = SimpleSchoolSerializer()
    classrooms = SimpleClassroomSerializer(many=True)

    class Meta:
        model = Teacher
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "school",
            "classrooms",
        ]


class CreateTeacherSerializer(serializers.ModelSerializer):
    school_id = serializers.ModelField(model_field=Teacher._meta.get_field("school"))
    classrooms_id = serializers.PrimaryKeyRelatedField(
        source="classrooms",
        queryset=Classroom.objects.all(),
        many=True,
    )

    class Meta:
        model = Teacher
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "school_id",
            "classrooms_id",
        ]

    def validate_school_id(self, value):
        if not School.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No school with the given ID was found.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            # Get classroom
            classrooms = validated_data.pop("classrooms")
            # Create new teacher first
            created_teacher = Teacher.objects.create(**validated_data)
            # Then add classrooms
            try:
                created_teacher.classrooms.add(*classrooms)
            except ValidationError as e:
                raise serializers.ValidationError({"classrooms_id": e})
            return created_teacher


class UpdateTeacherSerializer(CreateTeacherSerializer):
    class Meta(CreateTeacherSerializer.Meta):
        fields = [
            "first_name",
            "last_name",
            "gender",
            "school_id",
            "classrooms_id",
        ]

    def validate(self, attrs):
        if "school_id" in attrs:
            teacher = Teacher.objects.get(pk=self.context["teacher_id"])
            if teacher.school_id != attrs["school_id"]:
                if teacher.classrooms.count() > 0:
                    raise serializers.ValidationError(
                        {
                            "school_id": "To update school, teacher must not registered in any classroom."
                        }
                    )
        return super().validate(attrs)

    def update(self, instance, validated_data):
        with transaction.atomic():
            print(validated_data.get("school_id", instance.school))
            # Get classroom
            classrooms_data = validated_data.pop("classrooms")
            classrooms = instance.classrooms
            # Save first_name, last_name, gender, school first
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.last_name)
            instance.gender = validated_data.get("gender", instance.gender)
            school_id = validated_data.get("school_id", instance.school)
            instance.school = School.objects.get(pk=school_id)
            instance.save()
            # Then update classrooms
            try:
                classrooms.set(classrooms_data)
            except ValidationError as e:
                raise serializers.ValidationError({"classrooms_id": e})

            return instance
