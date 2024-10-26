from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ...models import Classroom
from ...filters import ClassroomFilter
from apis.serializers.classroom import (
    ClassroomSerializer,
    CreateClassroomSerializer,
    UpdateClassroomSerializer,
)


class ClassroomViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    queryset = (
        Classroom.objects.select_related("school")
        .prefetch_related("teachers", "students")
        .all()
    )
    serializer_class = ClassroomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClassroomFilter

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateClassroomSerializer
        elif self.request.method == "PATCH":
            return UpdateClassroomSerializer
        return ClassroomSerializer
