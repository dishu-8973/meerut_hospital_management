from django.conf import settings
from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.specialization}"

    @property
    def initials(self):
        """'Dr. Anil Verma' -> 'AV' (avatar ke liye)."""
        parts = self.name.split()
        if parts and parts[0].lower().rstrip(".") == "dr":
            parts = parts[1:]
        return "".join(p[0] for p in parts[:2]).upper() or "DR"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-appointment_date"]

    def __str__(self):
        return (
            f"{self.patient.username} - "
            f"{self.doctor.name} - {self.appointment_date}"
        )
