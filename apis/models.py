from django.core.validators import MaxValueValidator, MinValueValidator

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
