from django.contrib import admin
from . import models


@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "alias", "address"]
    list_filter = ["alias"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(models.Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ["grade", "room", "school"]
    list_filter = ["grade"]
    search_fields = ["school"]
    ordering = ["grade"]


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "gender",
        "school",
        "classroom",
    ]
    list_filter = ["classroom"]
    search_fields = ["first_name", "last_name"]
    ordering = ["first_name", "last_name"]

    def school(self, student):
        return student.classroom.school


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "gender", "school", "get_classrooms"]
    list_filter = ["classrooms"]
    search_fields = ["first_name", "last_name"]
    ordering = ["first_name", "last_name"]

    def get_classrooms(self, teacher):
        return ", ".join([str(classroom) for classroom in teacher.classrooms.all()])

    get_classrooms.short_description = "Classrooms"
