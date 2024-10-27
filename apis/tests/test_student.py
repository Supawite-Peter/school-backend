from apis.models import School, Classroom, Student, Teacher
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.fixture
def list_students(api_client):
    def do_list_students():
        return api_client.get("/api/v1/students/")

    return do_list_students


@pytest.fixture
def get_student(api_client):
    def do_get_student(id=1):
        return api_client.get(f"/api/v1/students/{id}/")

    return do_get_student


@pytest.fixture
def create_student(api_client):
    def do_create_student(student):
        return api_client.post("/api/v1/students/", student, format="json")

    return do_create_student


@pytest.fixture
def replace_student(api_client):
    def do_replace_student(id, student):
        return api_client.put(f"/api/v1/students/{id}/", student, format="json")

    return do_replace_student


@pytest.fixture
def update_student(api_client):
    def do_update_student(id, student):
        return api_client.patch(f"/api/v1/students/{id}/", student, format="json")

    return do_update_student


@pytest.fixture
def delete_student(api_client):
    def do_delete_student(id):
        return api_client.delete(
            f"/api/v1/students/{id}/",
            HTTP_ACCEPT="application/json",
        )

    return do_delete_student


@pytest.mark.django_db
class TestListStudents:
    def test_if_user_is_anonymous_return_401(self, list_students):
        response = list_students()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_students_exist_return_200(self, authenticate, list_students):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        student = baker.make(Student, classroom=classroom)

        response = list_students()

        assert response.status_code == status.HTTP_200_OK
        assert response.data[0] == {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "gender": student.gender,
            "school": {
                "id": school.id,
                "name": school.name,
                "alias": school.alias,
                "address": school.address,
            },
            "classroom": {
                "id": classroom.id,
                "grade": classroom.grade,
                "room": classroom.room,
            },
        }


@pytest.mark.django_db
class TestRetrieveStudent:
    def test_if_user_is_anonymous_return_401(self, get_student):
        response = get_student()

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_student_exist_return_200(self, authenticate, get_student):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        student = baker.make(Student, classroom=classroom)

        response = get_student(student.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "gender": student.gender,
            "school": {
                "id": school.id,
                "name": school.name,
                "alias": school.alias,
                "address": school.address,
            },
            "classroom": {
                "id": classroom.id,
                "grade": classroom.grade,
                "room": classroom.room,
            },
        }

    def test_if_student_not_exist_return_404(self, authenticate, get_student):
        authenticate()

        response = get_student(999)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateStudent:
    def test_if_user_is_anonymous_return_401(self, create_student):
        response = create_student({})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_student_is_created_return_201(self, authenticate, create_student):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)

        response = create_student(
            {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "M",
                "classroom_id": classroom.id,
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0
        assert response.data == {
            "id": response.data["id"],
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "classroom_id": classroom.id,
        }

    def test_if_full_name_is_not_unique_return_400(self, authenticate, create_student):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)
        baker.make(Student, first_name="John", last_name="Doe", classroom=classroom)

        response = create_student(
            {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "M",
                "classroom_id": classroom.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_first_name_is_missing_return_400(self, authenticate, create_student):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)

        response = create_student(
            {
                "last_name": "Doe",
                "gender": "M",
                "classroom_id": classroom.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_last_name_is_missing_return_400(self, authenticate, create_student):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)

        response = create_student(
            {
                "first_name": "John",
                "gender": "M",
                "classroom_id": classroom.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_gender_is_missing_return_400(self, authenticate, create_student):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)

        response = create_student(
            {"first_name": "John", "last_name": "Doe", "classroom_id": classroom.id}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_gender_is_invalid_return_400(self, authenticate, create_student):
        authenticate()
        school = baker.make(School)
        classroom = baker.make(Classroom, school=school)

        response = create_student(
            {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "X",
                "classroom_id": classroom.id,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_classroom_id_is_missing_return_400(self, authenticate, create_student):
        authenticate()

        response = create_student(
            {"first_name": "John", "last_name": "Doe", "gender": "M"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_classroom_id_is_not_exist_in_db_return_400(
        self, authenticate, create_student
    ):
        authenticate()

        response = create_student(
            {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "M",
                "classroom_id": 999,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestReplaceStudent:
    def test_if_user_is_anonymous_return_401(self, replace_student):
        response = replace_student(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_method_not_allowed(self, authenticate, replace_student):
        authenticate()

        response = replace_student(1, {})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestUpdateStudent:
    def test_if_user_is_anonymous_return_401(self, update_student):
        response = update_student(1, {})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_student_is_updated_return_200(self, authenticate, update_student):
        authenticate()
        classroom1 = baker.make(Classroom)
        classroom2 = baker.make(Classroom)
        student = baker.make(
            Student,
            first_name="Alice",
            last_name="Eve",
            gender="F",
            classroom=classroom1,
        )

        response = update_student(
            student.id,
            {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "M",
                "classroom_id": classroom2.id,
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "first_name": "John",
            "last_name": "Doe",
            "gender": "M",
            "classroom_id": classroom2.id,
        }

    def test_if_full_name_is_not_unique_return_400(self, authenticate, update_student):
        authenticate()
        student1 = baker.make(Student, first_name="Alice", last_name="Eve")
        student2 = baker.make(Student, first_name="John", last_name="Eve")

        response = update_student(
            student2.id,
            {
                "first_name": student1.first_name,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_gender_is_invalid_return_400(self, authenticate, update_student):
        authenticate()
        student = baker.make(Student, gender="F")

        response = update_student(
            student.id,
            {
                "gender": "X",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_classroom_id_is_not_exist_in_db_return_400(
        self, authenticate, update_student
    ):
        authenticate()
        student = baker.make(Student)

        response = update_student(
            student.id,
            {
                "classroom_id": 999,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteStudent:
    def test_if_user_is_anonymous_return_401(self, delete_student):
        response = delete_student(1)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_student_is_not_exist_in_db_return_404(
        self, authenticate, delete_student
    ):
        authenticate()
        response = delete_student(999)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_student_is_deleted_return_204(self, authenticate, delete_student):
        authenticate()
        student = baker.make(Student)

        response = delete_student(student.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
