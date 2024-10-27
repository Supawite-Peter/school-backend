from apis.models import School, Classroom, Student, Teacher
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.fixture
def list_schools(api_client):
    def do_list_schools():
        return api_client.get("/api/v1/schools/")

    return do_list_schools


@pytest.fixture
def get_school(api_client):
    def do_get_school(id=1):
        return api_client.get(f"/api/v1/schools/{id}/")

    return do_get_school


@pytest.fixture
def create_school(api_client):
    def do_create_school(school):
        return api_client.post("/api/v1/schools/", school, format="json")

    return do_create_school


@pytest.fixture
def replace_school(api_client):
    def do_replace_school(id, school):
        return api_client.put(f"/api/v1/schools/{id}/", school, format="json")

    return do_replace_school


@pytest.fixture
def update_school(api_client):
    def do_update_school(id, school):
        return api_client.patch(f"/api/v1/schools/{id}/", school, format="json")

    return do_update_school


@pytest.fixture
def delete_school(api_client):
    def do_delete_school(id):
        return api_client.delete(
            f"/api/v1/schools/{id}/",
            HTTP_ACCEPT="application/json",
        )

    return do_delete_school


@pytest.mark.django_db
class TestListSchool:

    def test_if_user_is_anonymous_return_401(self, list_schools):
        response = list_schools()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_school_exists_return_200(self, authenticate, list_schools):
        authenticate()
        school = baker.make(School)

        response = list_schools()

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0] == {
            "id": school.id,
            "name": school.name,
            "alias": school.alias,
            "address": school.address,
            "classrooms_count": 0,
            "students_count": 0,
            "teachers_count": 0,
        }

    def test_if_school_has_classrooms_return_classrooms_count(
        self, authenticate, list_schools
    ):
        authenticate()
        school = baker.make(School)
        baker.make(Classroom, school=school)
        baker.make(Classroom, school=school)

        response = list_schools()

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["classrooms_count"] == 2

    def test_if_school_has_teachers_return_teachers_count(
        self, authenticate, list_schools
    ):
        authenticate()
        school = baker.make(School)
        baker.make(Teacher, school=school)
        baker.make(Teacher, school=school)

        response = list_schools()

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["teachers_count"] == 2

    def test_if_school_has_students_return_students_count(
        self, authenticate, list_schools
    ):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        baker.make(Student, classroom=classroom)
        baker.make(Student, classroom=classroom)

        response = list_schools()

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["students_count"] == 2


@pytest.mark.django_db
class TestRetrieveSchool:

    def test_if_user_is_anonymous_return_401(self, get_school):
        response = get_school()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_school_exists_return_200(self, authenticate, get_school):
        authenticate()
        school = baker.make(School)

        response = get_school(school.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": school.id,
            "name": school.name,
            "alias": school.alias,
            "address": school.address,
            "classrooms_count": 0,
            "students_count": 0,
            "teachers_count": 0,
        }

    def test_if_school_has_classrooms_return_classrooms_count(
        self, authenticate, get_school
    ):
        authenticate()
        school = baker.make(School)
        baker.make(Classroom, school=school)
        baker.make(Classroom, school=school)

        response = get_school(school.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["classrooms_count"] == 2

    def test_if_school_has_teachers_return_teachers_count(
        self, authenticate, get_school
    ):
        authenticate()
        school = baker.make(School)
        baker.make(Teacher, school=school)
        baker.make(Teacher, school=school)

        response = get_school(school.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["teachers_count"] == 2

    def test_if_school_has_students_return_students_count(
        self, authenticate, get_school
    ):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        baker.make(Student, classroom=classroom)
        baker.make(Student, classroom=classroom)

        response = get_school(school.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["students_count"] == 2


@pytest.mark.django_db
class TestCreateSchool:
    def test_if_user_is_anonymous_return_401(self, create_school):
        response = create_school(
            {
                "name": "a",
                "alias": "b",
                "address": "c",
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_school_is_created_return_201(self, authenticate, create_school):
        authenticate()

        response = create_school(
            {
                "name": "Thai School",
                "alias": "TS",
                "address": "Bangkok, Thailand",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_if_school_is_missing_name_return_400(self, authenticate, create_school):
        authenticate()

        response = create_school(
            {
                "alias": "TS",
                "address": "Bangkok, Thailand",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_is_missing_alias_return_400(self, authenticate, create_school):
        authenticate()

        response = create_school(
            {
                "name": "Thai School",
                "address": "Bangkok, Thailand",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_is_missing_address_return_400(self, authenticate, create_school):
        authenticate()

        response = create_school(
            {
                "name": "Thai School",
                "alias": "TS",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_name_already_exists_return_400(
        self, authenticate, create_school
    ):
        authenticate()
        baker.make(School, name="a")

        response = create_school(
            {
                "name": "a",
                "alias": "b",
                "address": "c",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_alias_already_exists_return_400(
        self, authenticate, create_school
    ):
        authenticate()
        baker.make(School, alias="b")

        response = create_school(
            {
                "name": "a",
                "alias": "b",
                "address": "c",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestReplaceSchool:
    def test_if_user_is_anonymous_return_401(self, replace_school):
        response = replace_school(1, {"name": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_method_not_allowed(self, authenticate, replace_school):
        authenticate()

        response = replace_school(1, {"name": "a"})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestUpdateSchool:
    def test_if_user_is_anonymous_return_401(self, update_school):
        response = update_school(1, {"name": "a"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_school_does_not_exist_return_404(self, authenticate, update_school):
        authenticate()

        response = update_school(1, {"name": "a"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_school_is_updated_return_200(self, authenticate, update_school):
        authenticate()
        school = baker.make(School)

        response = update_school(school.id, {"name": "a", "alias": "b", "address": "c"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "name": "a",
            "alias": "b",
            "address": "c",
        }

    def test_if_school_name_already_exists_return_400(
        self, authenticate, update_school
    ):
        authenticate()
        baker.make(School, name="a")
        school = baker.make(School)

        response = update_school(school.id, {"name": "a"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_alias_already_exists_return_400(
        self, authenticate, update_school
    ):
        authenticate()
        baker.make(School, alias="b")
        school = baker.make(School)

        response = update_school(school.id, {"alias": "b"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteSchool:
    def test_if_user_is_anonymous_return_401(self, delete_school):
        response = delete_school(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_school_does_not_exist_return_404(self, authenticate, delete_school):
        authenticate()

        response = delete_school(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_school_is_deleted_return_204(self, authenticate, delete_school):
        authenticate()
        school = baker.make(School)

        response = delete_school(school.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
