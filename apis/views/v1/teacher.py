from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ...models import Teacher
from ...filters import TeacherFilter
from ...serializers import TeacherSerializer


class TeacherViewSet(ModelViewSet):
    queryset = (
        Teacher.objects.select_related("school").prefetch_related("classrooms").all()
    )
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter
