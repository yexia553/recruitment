"""
关于ModelFrom的介绍参考：https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/
"""

from django.forms import ModelForm
from jobs.models import Resume


class ResumeForm(ModelForm):
    class Meta:
        model = Resume

        fields = ["username", "city", "phone", "email",
                  "apply_position", "born_address", "gender",
                  "picture", "attachment","bachelor_school",
                  "master_school", "major", "degree", "candidate_introduction",
                  "work_experience", "project_experience"]
