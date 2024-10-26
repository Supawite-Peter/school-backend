# Generated by Django 5.0.4 on 2024-10-22 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apis", "0002_rename_teacher_classrooms"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="school",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teachers",
                to="apis.school",
            ),
            preserve_default=False,
        ),
    ]
