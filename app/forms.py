from django import forms
from .models import JobModel

class JobForm(forms.ModelForm):
    class Meta:
        model = JobModel
        fields = ['position', 'company', 'description', 'requirements', 'last_apply_date', 'pay_rate', 'max_applicant', 'is_active']

