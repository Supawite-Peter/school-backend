from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ...models import School
from ...filters import SchoolFilter
from ...serializers import SchoolSerializer


class SchoolViewSet(ModelViewSet):
    queryset = School.objects.prefetch_related(
        "classrooms", "classrooms__students", "teachers"
    ).all()
    serializer_class = SchoolSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SchoolFilter
