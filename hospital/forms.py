from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Appointment, Doctor


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": "Choose a username",
            "email": "you@example.com",
            "password1": "Create a password",
            "password2": "Repeat the password",
        }
        for name, text in placeholders.items():
            self.fields[name].widget.attrs["placeholder"] = text

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Is email se account pehle se bana hua hai.")
        return email


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        label="Date and time",
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Appointment
        fields = ["doctor", "appointment_date", "reason"]
        labels = {"reason": "Reason for visit"}
        widgets = {
            "reason": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Briefly describe your symptoms or concern"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = Doctor.objects.filter(available=True)
        self.fields["doctor"].empty_label = "Select a doctor"

    def clean_appointment_date(self):
        value = self.cleaned_data["appointment_date"]
        if value <= timezone.now():
            raise ValidationError("Appointment ka time future mein hona chahiye.")
        return value

    def clean(self):
        cleaned = super().clean()
        doctor = cleaned.get("doctor")
        when = cleaned.get("appointment_date")
        if doctor and when:
            slot_taken = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=when,
                status__in=["Pending", "Confirmed"],
            ).exists()
            if slot_taken:
                raise ValidationError(
                    "Is doctor ka yeh slot already booked hai. Koi aur time chuniye."
                )
        return cleaned
