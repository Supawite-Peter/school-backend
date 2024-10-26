from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ...models import Student
from ...filters import StudentFilter
from ...serializers import StudentSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.select_related("classroom", "classroom__school").all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
