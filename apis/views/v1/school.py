from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from ...models import School
from ...filters import SchoolFilter
from apis.serializers.school import SchoolSerializer, CreateUpdateSchoolSerializer


class SchoolViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    queryset = School.objects.prefetch_related(
        "classrooms", "classrooms__students", "teachers"
    ).all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return CreateUpdateSchoolSerializer
        return SchoolSerializer
