from apis.models import School, Classroom, Teacher
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.fixture
def list_teachers(api_client):
    def do_list_teachers():
        return api_client.get("/api/v1/teachers/")

    return do_list_teachers


@pytest.fixture
def get_teacher(api_client):
    def do_get_teacher(id=1):
        return api_client.get(f"/api/v1/teachers/{id}/")

    return do_get_teacher


@pytest.fixture
def create_teacher(api_client):
    def do_create_teacher(teacher):
        return api_client.post("/api/v1/teachers/", teacher, format="json")

    return do_create_teacher


@pytest.fixture
def replace_teacher(api_client):
    def do_replace_teacher(id, teacher):
        return api_client.put(f"/api/v1/teachers/{id}/", teacher, format="json")

    return do_replace_teacher


@pytest.fixture
def update_teacher(api_client):
    def do_update_teacher(id, teacher):
        return api_client.patch(f"/api/v1/teachers/{id}/", teacher, format="json")

    return do_update_teacher


@pytest.fixture
def delete_teacher(api_client):
    def do_delete_teacher(id):
        return api_client.delete(
            f"/api/v1/teachers/{id}/",
            HTTP_ACCEPT="application/json",
        )

    return do_delete_teacher


@pytest.mark.django_db
class TestListTeachers:
    def test_if_user_is_anonymous_return_401(self, list_teachers):
        response = list_teachers()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_teachers_exist_return_200(self, authenticate, list_teachers):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        teacher = baker.make(Teacher, school=school, classrooms=[classroom])

        response = list_teachers()

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0] == {
            "id": teacher.id,
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "gender": teacher.gender,
            "school": {
                "id": teacher.school.id,
                "name": teacher.school.name,
                "alias": teacher.school.alias,
                "address": teacher.school.address,
            },
            "classrooms": [
                {
                    "id": classroom.id,
                    "grade": classroom.grade,
                    "room": classroom.room,
                }
            ],
        }

    def test_if_teacher_registered_to_multiple_classrooms_return_classrooms_list(
        self, authenticate, list_teachers
    ):
        authenticate()
        school = baker.make(School)
        classroom1 = baker.make(Classroom, school=school)
        classroom2 = baker.make(Classroom, school=school)
        baker.make(Teacher, school=school, classrooms=[classroom1, classroom2])

        response = list_teachers()

        response_classrooms = response.data[0]["classrooms"]
        assert_classrooms = [
            {
                "id": classroom1.id,
                "grade": classroom1.grade,
                "room": classroom1.room,
            },
            {
                "id": classroom2.id,
                "grade": classroom2.grade,
                "room": classroom2.room,
            },
        ]
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response_classrooms, list)
        assert {frozenset(item.items()) for item in response_classrooms} == {
            frozenset(item.items()) for item in assert_classrooms
        }


@pytest.mark.django_db
class TestRetrieveTeacher:
    def test_if_user_is_anonymous_return_401(self, get_teacher):
        response = get_teacher()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_teacher_not_exist_return_404(self, authenticate, get_teacher):
        authenticate()
        response = get_teacher(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_teacher_exist_return_200(self, authenticate, get_teacher):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        teacher = baker.make(Teacher, school=school, classrooms=[classroom])

        response = get_teacher(teacher.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": teacher.id,
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "gender": teacher.gender,
            "school": {
                "id": teacher.school.id,
                "name": teacher.school.name,
                "alias": teacher.school.alias,
                "address": teacher.school.address,
            },
            "classrooms": [
                {
                    "id": classroom.id,
                    "grade": classroom.grade,
                    "room": classroom.room,
                }
            ],
        }

    def test_if_teacher_registered_to_multiple_classrooms_return_classrooms_list(
        self, authenticate, get_teacher
    ):
        authenticate()
        school = baker.make(School)
        classroom1 = baker.make(Classroom, school=school)
        classroom2 = baker.make(Classroom, school=school)
        teacher = baker.make(
            Teacher, school=school, classrooms=[classroom1, classroom2]
        )

        response = get_teacher(teacher.id)

        response_classrooms = response.data["classrooms"]
        assert_classrooms = [
            {
                "id": classroom1.id,
                "grade": classroom1.grade,
                "room": classroom1.room,
            },
            {
                "id": classroom2.id,
                "grade": classroom2.grade,
                "room": classroom2.room,
            },
        ]
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response_classrooms, list)
        assert {frozenset(item.items()) for item in response_classrooms} == {
            frozenset(item.items()) for item in assert_classrooms
        }


@pytest.mark.django_db
class TestCreateTeacher:
    def test_if_user_is_anonymous_return_401(self, create_teacher):
        response = create_teacher({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_teacher_created_return_201(self, authenticate, create_teacher):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)

        response = create_teacher(
            {
                "school_id": school.id,
                "first_name": "a",
                "last_name": "b",
                "gender": "F",
                "classrooms_id": [classroom.id],
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        assert response.data == {
            "id": response.data["id"],
            "first_name": "a",
            "last_name": "b",
            "gender": "F",
            "school_id": school.id,
            "classrooms_id": [classroom.id],
        }

    def test_if_school_id_and_classrooms_id_are_mismatch_return_400(
        self, authenticate, create_teacher
    ):
        authenticate()
        school1 = baker.make(School)
        school2 = baker.make(School)
        classroom = baker.make(Classroom, school=school2)

        response = create_teacher(
            {
                "first_name": "a",
                "last_name": "b",
                "gender": "F",
                "school_id": school1.id,
                "classrooms_id": [classroom.id],
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_full_name_is_not_unique_return_400(self, authenticate, create_teacher):
        authenticate()
        school = baker.make(School)
        baker.make(Teacher, school=school, first_name="a", last_name="b")

        response = create_teacher(
            {
                "first_name": "a",
                "last_name": "b",
                "gender": "F",
                "school_id": school.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_classrooms_id_are_not_provide_return_201(
        self, authenticate, create_teacher
    ):
        authenticate()
        school = baker.make(School)

        response = create_teacher(
            {
                "first_name": "a",
                "last_name": "b",
                "gender": "F",
                "school_id": school.id,
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["classrooms_id"] == []

    def test_if_classrooms_id_is_not_exist_in_database_return_400(
        self, authenticate, create_teacher
    ):
        authenticate()
        school = baker.make(School)
        baker.make(Classroom, school=school, id=100)

        response = create_teacher(
            {
                "first_name": "a",
                "last_name": "b",
                "gender": "F",
                "school_id": school.id,
                "classrooms_id": [1],
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_first_name_is_not_provide_return_400(
        self, authenticate, create_teacher
    ):
        authenticate()
        school = baker.make(School)

        response = create_teacher(
            {
                "last_name": "b",
                "gender": "F",
                "school_id": school.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_last_name_is_not_provide_return_400(self, authenticate, create_teacher):
        authenticate()
        school = baker.make(School)

        response = create_teacher(
            {
                "first_name": "a",
                "gender": "F",
                "school_id": school.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_gender_is_not_provide_return_400(self, authenticate, create_teacher):
        authenticate()
        school = baker.make(School)

        response = create_teacher(
            {
                "first_name": "a",
                "last_name": "b",
                "school_id": school.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_gender_is_invalid_return_400(self, authenticate, create_teacher):
        authenticate()
        school = baker.make(School)

        response = create_teacher(
            {
                "first_name": "a",
                "last_name": "b",
                "gender": "X",
                "school_id": school.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_id_is_not_provide_return_400(self, authenticate, create_teacher):
        authenticate()

        response = create_teacher(
            {
                "first_name": "a",
                "last_name": "b",
                "gender": "F",
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_school_id_is_not_exist_in_database_return_400(
        self, authenticate, create_teacher
    ):
        authenticate()
        baker.make(School, id=100)

        response = create_teacher(
            {
                "first_name": "a",
                "last_name": "b",
                "gender": "F",
                "school_id": 1,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestReplaceTeacher:
    def test_if_user_is_anonymous_return_401(self, replace_teacher):
        response = replace_teacher(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_method_not_allowed(self, authenticate, replace_teacher):
        authenticate()

        response = replace_teacher(1, {})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestUpdateTeacher:
    def test_if_user_is_anonymous_return_401(self, update_teacher):
        response = update_teacher(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_teacher_is_not_exist_return_404(self, authenticate, update_teacher):
        authenticate()
        response = update_teacher(1, {})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_teacher_updated_return_200(self, authenticate, update_teacher):
        authenticate()
        teacher = baker.make(
            Teacher, first_name="a", last_name="b", gender="M", classrooms=[]
        )

        response = update_teacher(
            teacher.id, {"first_name": "c", "last_name": "d", "gender": "F"}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "first_name": "c",
            "last_name": "d",
            "gender": "F",
            "school_id": teacher.school_id,
            "classrooms_id": [],
        }

    def test_if_full_name_is_not_unique_return_400(self, authenticate, update_teacher):
        authenticate()
        baker.make(Teacher, first_name="c", last_name="b")
        teacher = baker.make(Teacher, first_name="a", last_name="b")

        response = update_teacher(teacher.id, {"first_name": "c"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_try_to_update_school_but_teacher_still_have_classrooms_return_400(
        self, authenticate, update_teacher
    ):
        authenticate()
        school1 = baker.make(School)
        school2 = baker.make(School)
        classroom = baker.make(Classroom, school=school1)
        teacher = baker.make(Teacher, school=school1, classrooms=[classroom])

        response = update_teacher(teacher.id, {"school_id": school2.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_try_to_update_school_but_teacher_does_not_have_classrooms_return_200(
        self, authenticate, update_teacher
    ):
        authenticate()
        school1 = baker.make(School)
        school2 = baker.make(School)
        teacher = baker.make(Teacher, school=school1, classrooms=[])

        response = update_teacher(teacher.id, {"school_id": school2.id})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["school_id"] == school2.id

    def test_if_school_id_is_not_exist_in_database_return_400(
        self, authenticate, update_teacher
    ):
        authenticate()
        school = baker.make(School, id=100)
        teacher = baker.make(
            Teacher, first_name="a", last_name="b", school=school, classrooms=[]
        )

        response = update_teacher(teacher.id, {"school_id": 1})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_gender_is_invalid_return_400(self, authenticate, update_teacher):
        authenticate()
        teacher = baker.make(Teacher, first_name="a", last_name="b")

        response = update_teacher(teacher.id, {"gender": "X"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_classrooms_id_are_not_exist_in_database_return_400(
        self, authenticate, update_teacher
    ):
        authenticate()
        classroom = baker.make(Classroom, id=100)
        teacher = baker.make(
            Teacher, first_name="a", last_name="b", classrooms=[classroom]
        )

        response = update_teacher(teacher.id, {"classrooms_id": [classroom.id, 1]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_classrooms_id_are_mismatch_with_teacher_school_return_400(
        self, authenticate, update_teacher
    ):
        authenticate()
        school1 = baker.make(School)
        school2 = baker.make(School)
        classroom1 = baker.make(Classroom, school=school1)
        classroom2 = baker.make(Classroom, school=school2)
        teacher = baker.make(Teacher, school=school1, classrooms=[classroom1])

        response = update_teacher(
            teacher.id, {"classrooms_id": [classroom1.id, classroom2.id]}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteTeacher:
    def test_if_user_is_anonymous_return_401(self, delete_teacher):
        response = delete_teacher(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_teacher_is_not_exist_return_404(self, authenticate, delete_teacher):
        authenticate()
        response = delete_teacher(1)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_teacher_deleted_return_204(self, authenticate, delete_teacher):
        authenticate()
        teacher = baker.make(Teacher)

        response = delete_teacher(teacher.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
