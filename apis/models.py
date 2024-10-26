from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.db import models


GENDER_MALE = "M"
GENDER_FEMALE = "F"
GENDER_OTHER = "O"

GENDER_CHOICES = (
    (GENDER_MALE, "Male"),
    (GENDER_FEMALE, "Female"),
    (GENDER_OTHER, "Other"),
)


class School(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Classroom(models.Model):
    grade = models.IntegerField(
        validators=[MaxValueValidator(12), MinValueValidator(1)]
    )
    room = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="classrooms"
    )

    def __str__(self):
        return f"{self.grade}/{self.room}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["grade", "room", "school"],
                name="unique_classroom",
            )
        ]
        ordering = ["grade", "room"]


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="teachers"
    )
    classrooms = models.ManyToManyField(
        Classroom,
        related_name="teachers",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"], name="teacher_full_name"
            )
        ]
        ordering = ["first_name", "last_name"]


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="students"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["first_name", "last_name"], name="student_full_name"
            ),
        ]
        ordering = ["first_name", "last_name"]


def m2mClassroomTeacherValidator(sender, **kwargs):
    """
    Validates that the classrooms being added to a teacher belong to the same
    school as the teacher. This function is triggered on the 'pre_add' action
    of the ManyToMany relationship between teachers and classrooms.

    Args:
        sender (Model): The model class that triggered the signal.
        **kwargs: Arbitrary keyword arguments containing 'instance', 'pk_set',
                  and 'action'.

    Raises:
        ValidationError: If any classroom being added does not belong to the
                         same school as the teacher.
    """
    # Teacher instace
    instance = kwargs["instance"]
    # Classroom pk_set
    pk_set = kwargs["pk_set"]
    action = kwargs["action"]
    # School pk of the incoming classroom
    classrooms_school_pk = list(
        sender.objects.filter(classroom_id__in=pk_set).values_list(
            "classroom__school__pk", flat=True
        )
    )
    if action == "pre_add":
        # Check if all classrooms belong to the same school as the teacher
        if not all(
            instance.school.pk == school_pk for school_pk in classrooms_school_pk
        ):
            raise ValidationError(
                "The school of the classroom must be the same as the school of the teacher"
            )


# Add validator to the m2m signal of the Classroom and Teacher models
m2m_changed.connect(m2mClassroomTeacherValidator, sender=Classroom.teachers.through)
