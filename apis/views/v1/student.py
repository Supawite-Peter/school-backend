from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ...models import Student
from ...filters import StudentFilter
from apis.serializers.student import (
    StudentSerializer,
    CreateStudentSerializer,
    UpdateStudentSerializer,
)


class StudentViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    queryset = Student.objects.select_related("classroom", "classroom__school").all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateStudentSerializer
        elif self.request.method == "PATCH":
            return UpdateStudentSerializer
        return StudentSerializer
