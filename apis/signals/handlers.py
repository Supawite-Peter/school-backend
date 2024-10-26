from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from apis.models import Classroom


@receiver(m2m_changed, sender=Classroom.teachers.through)
def classroom_teacher_validator(sender, **kwargs):
    """
    Validates that the classrooms being added to a teacher belong to the same
    school as the teacher. This function is triggered on the 'pre_add' action
    of the ManyToMany relationship between teachers and classrooms.

    Args:
        sender (Model): The model class that triggered the signal.
        **kwargs: Arbitrary keyword arguments containing 'instance', 'pk_set',
                  and 'action'.

    Raises:
        ValidationError: If any classroom being added does not belong to the
                         same school as the teacher.
    """
    # Teacher instace
    instance = kwargs["instance"]
    # Classroom pk_set
    pk_set = kwargs["pk_set"]
    action = kwargs["action"]
    # School pk of the incoming classroom
    classrooms_school_pk = list(
        sender.objects.filter(classroom_id__in=pk_set).values_list(
            "classroom__school__pk", flat=True
        )
    )
    if action == "pre_add":
        # Check if all classrooms belong to the same school as the teacher
        if not all(
            instance.school.pk == school_pk for school_pk in classrooms_school_pk
        ):
            raise ValidationError(
                "The school of the classroom must be the same as the school of the teacher"
            )
