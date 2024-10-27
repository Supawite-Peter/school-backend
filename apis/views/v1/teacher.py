from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ...models import Teacher
from ...filters import TeacherFilter
from apis.serializers.teacher import (
    TeacherSerializer,
    CreateTeacherSerializer,
    UpdateTeacherSerializer,
)


class TeacherViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    queryset = (
        Teacher.objects.select_related("school").prefetch_related("classrooms").all()
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateTeacherSerializer
        elif self.request.method == "PATCH":
            return UpdateTeacherSerializer
        return TeacherSerializer

    def get_serializer_context(self):
        return {"teacher_id": self.kwargs["pk"]}
