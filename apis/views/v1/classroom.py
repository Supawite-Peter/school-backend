from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ...models import Classroom
from ...filters import ClassroomFilter
from ...serializers import ClassroomSerializer


class ClassroomViewSet(ModelViewSet):
    queryset = (
        Classroom.objects.select_related("school")
        .prefetch_related("teachers", "students")
        .all()
    )
    serializer_class = ClassroomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClassroomFilter
