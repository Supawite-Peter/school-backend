from apis.models import School, Classroom, Student, Teacher
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.fixture
def list_classrooms(api_client):
    def do_list_classrooms():
        return api_client.get("/api/v1/classrooms/")

    return do_list_classrooms


@pytest.fixture
def get_classroom(api_client):
    def do_get_classroom(id=1):
        return api_client.get(f"/api/v1/classrooms/{id}/")

    return do_get_classroom


@pytest.fixture
def create_classroom(api_client):
    def do_create_classroom(classroom):
        return api_client.post("/api/v1/classrooms/", classroom, format="json")

    return do_create_classroom


@pytest.fixture
def replace_classroom(api_client):
    def do_replace_classroom(id, classroom):
        return api_client.put(f"/api/v1/classrooms/{id}/", classroom, format="json")

    return do_replace_classroom


@pytest.fixture
def update_classroom(api_client):
    def do_update_classroom(id, classroom):
        return api_client.patch(f"/api/v1/classrooms/{id}/", classroom, format="json")

    return do_update_classroom


@pytest.fixture
def delete_classroom(api_client):
    def do_delete_classroom(id):
        return api_client.delete(
            f"/api/v1/classrooms/{id}/",
            HTTP_ACCEPT="application/json",
        )

    return do_delete_classroom


@pytest.mark.django_db
class TestListClassrooms:
    def test_if_user_is_anonymous_return_401(self, list_classrooms):
        response = list_classrooms()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_classroom_exists_return_200(self, authenticate, list_classrooms):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)

        response = list_classrooms()

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0] == {
            "id": classroom.id,
            "grade": classroom.grade,
            "room": classroom.room,
            "school": {
                "id": school.id,
                "name": school.name,
                "alias": school.alias,
                "address": school.address,
            },
            "students": [],
            "teachers": [],
        }

    def test_if_teachers_registered_in_classroom_return_teachers_details(
        self, authenticate, list_classrooms
    ):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        teacher1 = baker.make(Teacher, school=school, classrooms=[classroom])
        teacher2 = baker.make(Teacher, school=school, classrooms=[classroom])

        response = list_classrooms()

        response_teachers = response.data[0]["teachers"]
        assert_teachers = [
            {
                "id": teacher1.id,
                "first_name": teacher1.first_name,
                "last_name": teacher1.last_name,
                "gender": teacher1.gender,
            },
            {
                "id": teacher2.id,
                "first_name": teacher2.first_name,
                "last_name": teacher2.last_name,
                "gender": teacher2.gender,
            },
        ]
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data[0]["teachers"], list)
        assert {frozenset(item.items()) for item in response_teachers} == {
            frozenset(item.items()) for item in assert_teachers
        }

    def test_if_students_registered_in_classroom_return_students_details(
        self, authenticate, list_classrooms
    ):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        student1 = baker.make(Student, classroom=classroom)
        student2 = baker.make(Student, classroom=classroom)

        response = list_classrooms()

        response_students = response.data[0]["students"]
        assert_students = [
            {
                "id": student1.id,
                "first_name": student1.first_name,
                "last_name": student1.last_name,
                "gender": student1.gender,
            },
            {
                "id": student2.id,
                "first_name": student2.first_name,
                "last_name": student2.last_name,
                "gender": student2.gender,
            },
        ]
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data[0]["students"], list)
        assert {frozenset(item.items()) for item in response_students} == {
            frozenset(item.items()) for item in assert_students
        }


@pytest.mark.django_db
class TestRetrieveClassroom:
    def test_if_user_is_anonymous_return_401(self, get_classroom):
        response = get_classroom()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_classroom_not_found_return_404(self, authenticate, get_classroom):
        authenticate()

        response = get_classroom()

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_classroom_exists_return_200(self, authenticate, get_classroom):
        authenticate()
        classroom = baker.make(Classroom)

        response = get_classroom(classroom.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": classroom.id,
            "grade": classroom.grade,
            "room": classroom.room,
            "school": {
                "id": classroom.school.id,
                "name": classroom.school.name,
                "alias": classroom.school.alias,
                "address": classroom.school.address,
            },
            "students": [],
            "teachers": [],
        }

    def test_if_teachers_registered_in_classroom_return_teachers_details(
        self, authenticate, get_classroom
    ):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        teacher1 = baker.make(Teacher, school=school, classrooms=[classroom])
        teacher2 = baker.make(Teacher, school=school, classrooms=[classroom])

        response = get_classroom(classroom.id)

        response_teachers = response.data["teachers"]
        assert_teachers = [
            {
                "id": teacher1.id,
                "first_name": teacher1.first_name,
                "last_name": teacher1.last_name,
                "gender": teacher1.gender,
            },
            {
                "id": teacher2.id,
                "first_name": teacher2.first_name,
                "last_name": teacher2.last_name,
                "gender": teacher2.gender,
            },
        ]
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["teachers"], list)
        assert {frozenset(item.items()) for item in response_teachers} == {
            frozenset(item.items()) for item in assert_teachers
        }

    def test_if_students_registered_in_classroom_return_students_details(
        self, authenticate, get_classroom
    ):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        student1 = baker.make(Student, classroom=classroom)
        student2 = baker.make(Student, classroom=classroom)

        response = get_classroom(classroom.id)

        response_students = response.data["students"]
        assert_students = [
            {
                "id": student1.id,
                "first_name": student1.first_name,
                "last_name": student1.last_name,
                "gender": student1.gender,
            },
            {
                "id": student2.id,
                "first_name": student2.first_name,
                "last_name": student2.last_name,
                "gender": student2.gender,
            },
        ]
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data["students"], list)
        assert {frozenset(item.items()) for item in response_students} == {
            frozenset(item.items()) for item in assert_students
        }


@pytest.mark.django_db
class TestCreateClassroom:
    def test_if_user_is_anonymous_return_401(self, create_classroom):
        response = create_classroom({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_classroom_created_return_201(self, authenticate, create_classroom):
        authenticate()
        school = baker.make(School)

        response = create_classroom({"grade": 1, "room": 1, "school_id": school.id})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        assert response.data["grade"] == 1
        assert response.data["room"] == 1
        assert response.data["school_id"] == school.id

    def test_if_classroom_already_exists_return_400(
        self, authenticate, create_classroom
    ):
        authenticate()
        school = baker.make(School)
        baker.make(Classroom, grade=1, room=1, school=school)

        response = create_classroom({"grade": 1, "room": 1, "school_id": school.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_grade_is_missing_return_400(self, authenticate, create_classroom):
        authenticate()
        school = baker.make(School)

        response = create_classroom({"room": 1, "school_id": school.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_room_is_missing_return_400(self, authenticate, create_classroom):
        authenticate()
        school = baker.make(School)

        response = create_classroom({"grade": 1, "school_id": school.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_id_is_missing_return_400(self, authenticate, create_classroom):
        authenticate()

        response = create_classroom({"grade": 1, "room": 1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_id_is_not_exist_in_database_return_400(
        self, authenticate, create_classroom
    ):
        authenticate()
        baker.make(School, id=100)

        response = create_classroom({"grade": 1, "room": 1, "school_id": 1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_classroom_grade_is_bigger_than_12_return_400(
        self, authenticate, create_classroom
    ):
        authenticate()
        school = baker.make(School)

        response = create_classroom({"grade": 13, "room": 1, "school_id": school.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_classroom_grade_is_lower_than_1_return_400(
        self, authenticate, create_classroom
    ):
        authenticate()
        school = baker.make(School)

        response = create_classroom({"grade": 0, "room": 1, "school_id": school.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestReplaceClassroom:
    def test_if_user_is_anonymous_return_401(self, replace_classroom):
        response = replace_classroom(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_method_not_allowed(self, authenticate, replace_classroom):
        authenticate()

        response = replace_classroom(1, {})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestUpdateClassroom:
    def test_if_user_is_anonymous_return_401(self, update_classroom):
        response = update_classroom(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_classroom_not_exists_return_404(self, authenticate, update_classroom):
        authenticate()

        response = update_classroom(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_classroom_updated_return_200(self, authenticate, update_classroom):
        authenticate()
        classroom = baker.make(Classroom, grade=1, room=1)

        response = update_classroom(classroom.id, {"grade": 2, "room": 2})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "grade": 2,
            "room": 2,
        }

    def test_if_updated_classroom_already_exists_return_400(
        self, authenticate, update_classroom
    ):
        authenticate()
        school = baker.make(School)
        classroom1 = baker.make(Classroom, grade=1, room=1, school=school)
        baker.make(Classroom, grade=2, room=2, school=school)

        response = update_classroom(classroom1.id, {"grade": 2, "room": 2})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteClassroom:
    def test_if_user_is_anonymous_return_401(self, delete_classroom):
        response = delete_classroom(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_classroom_not_exists_return_404(self, authenticate, delete_classroom):
        authenticate()

        response = delete_classroom(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_classroom_deleted_return_204(self, authenticate, delete_classroom):
        authenticate()
        classroom = baker.make(Classroom)

        response = delete_classroom(classroom.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
