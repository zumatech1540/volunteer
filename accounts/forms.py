from django import forms
from .models import Task, Event, Voter

from .models import User

# ================= TASK FORM =================
class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'assigned_to',
            'event',
            'priority',
            'due_date',
            'status'
        ]


# ================= EVENT FORM =================
class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date']


# ================= VOTER FORM =================
class VoterForm(forms.ModelForm):

    class Meta:
        model = Voter
        fields = [
            'first_name',
            'last_name',
            'phone',
            'id_number',
            'ward',
            'polling_station',
            'support_status',
            'notes'
        ]




class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    constituency = forms.IntegerField(required=False)
    ward = forms.IntegerField(required=False)
    polling_station = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'role']

    def clean(self):
        cleaned = super().clean()

        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match")

        return cleaned