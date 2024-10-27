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
        required=False,
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

    def validate(self, attrs, school_id=None):
        if "classrooms" in attrs:
            if school_id is None:
                school_id = attrs["school_id"]
            school_classrooms = list(School.objects.get(pk=school_id).classrooms.all())
            for classroom_id in attrs["classrooms"]:
                if classroom_id not in school_classrooms:
                    raise serializers.ValidationError(
                        {
                            "classrooms_id": [
                                "The school of the classroom must be the same as the school of the teacher."
                            ],
                        }
                    )
        return super().validate(attrs)

    def create(self, validated_data):
        with transaction.atomic():
            # Get classroom
            classrooms = None
            if "classrooms" in validated_data:
                classrooms = validated_data.pop("classrooms")
            # Create new teacher first
            created_teacher = Teacher.objects.create(**validated_data)
            # Then add classrooms
            if classrooms is not None:
                try:
                    created_teacher.classrooms.add(*classrooms)
                except ValidationError as e:
                    raise serializers.ValidationError({"classrooms_id": list(e)})
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
        return super().validate(attrs, school_id=self.context["teacher_id"])

    def update(self, instance, validated_data):
        with transaction.atomic():
            # Get classroom
            classrooms_data = None
            if "classrooms" in validated_data:
                classrooms_data = validated_data.pop("classrooms")
                classrooms = instance.classrooms
            # Save first_name, last_name, gender, school first
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.last_name)
            instance.gender = validated_data.get("gender", instance.gender)
            if "school_id" in validated_data:
                school_id = validated_data.get("school_id")
                instance.school = School.objects.get(pk=school_id)
            instance.save()
            # Then update classrooms
            if classrooms_data is not None:
                try:
                    classrooms.set(classrooms_data)
                except ValidationError as e:
                    raise serializers.ValidationError({"classrooms_id": list(e)})

            return instance
