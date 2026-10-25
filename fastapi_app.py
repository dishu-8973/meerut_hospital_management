"""
Meerut Hospital REST API (FastAPI)

Ye server Django ke same database aur models ko use karta hai.
Pehle Django migrations chalao, phir:

    python -m uvicorn fastapi_app:app --reload --port 8001

Docs: http://127.0.0.1:8001/docs
"""
import os
from datetime import datetime
from typing import List

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import authenticate  # noqa: E402
from django.utils import timezone  # noqa: E402

from fastapi import Depends, FastAPI, HTTPException  # noqa: E402
from fastapi import status as http_status  # noqa: E402
from fastapi.security import HTTPBasic, HTTPBasicCredentials  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from hospital.models import Appointment, Doctor  # noqa: E402


app = FastAPI(
    title="Meerut Hospital API",
    description="Doctors and patient appointment APIs",
    version="1.0.0",
)

security = HTTPBasic()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class DoctorOut(BaseModel):
    id: int
    name: str
    specialization: str
    experience: int
    description: str


class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: datetime
    reason: str = Field(min_length=3, max_length=1000)


class AppointmentOut(BaseModel):
    id: int
    doctor_id: int
    doctor_name: str
    specialization: str
    appointment_date: datetime
    reason: str
    status: str
    created_at: datetime


def appointment_to_schema(appointment: Appointment) -> AppointmentOut:
    return AppointmentOut(
        id=appointment.id,
        doctor_id=appointment.doctor_id,
        doctor_name=appointment.doctor.name,
        specialization=appointment.doctor.specialization,
        appointment_date=appointment.appointment_date,
        reason=appointment.reason,
        status=appointment.status,
        created_at=appointment.created_at,
    )


# ---------------------------------------------------------------------------
# Authentication (Django ke existing users, HTTP Basic)
# NOTE: Basic auth sirf HTTPS par use karo (production).
# ---------------------------------------------------------------------------
def get_patient(credentials: HTTPBasicCredentials = Depends(security)):
    user = authenticate(
        username=credentials.username,
        password=credentials.password,
    )
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=http_status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


# ---------------------------------------------------------------------------
# Endpoints
# (plain `def` use kiya hai kyunki Django ORM synchronous hai; FastAPI inhe
#  threadpool mein chalata hai.)
# ---------------------------------------------------------------------------
@app.get("/")
def api_home():
    return {"message": "Meerut Hospital API is running", "docs": "/docs"}


@app.get("/api/doctors", response_model=List[DoctorOut])
def list_doctors():
    doctors = Doctor.objects.filter(available=True).order_by("name")
    return [
        DoctorOut(
            id=d.id,
            name=d.name,
            specialization=d.specialization,
            experience=d.experience,
            description=d.description,
        )
        for d in doctors
    ]


@app.get("/api/appointments", response_model=List[AppointmentOut])
def list_my_appointments(patient=Depends(get_patient)):
    appointments = (
        Appointment.objects.filter(patient=patient)
        .select_related("doctor")
        .order_by("-appointment_date")
    )
    return [appointment_to_schema(a) for a in appointments]


@app.post(
    "/api/appointments",
    response_model=AppointmentOut,
    status_code=http_status.HTTP_201_CREATED,
)
def create_appointment(payload: AppointmentCreate, patient=Depends(get_patient)):
    doctor = Doctor.objects.filter(id=payload.doctor_id, available=True).first()
    if doctor is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Doctor not found or not available",
        )

    when = payload.appointment_date
    if timezone.is_naive(when):
        when = timezone.make_aware(when)

    if when <= timezone.now():
        raise HTTPException(
            status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="appointment_date must be in the future",
        )

    slot_taken = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=when,
        status__in=["Pending", "Confirmed"],
    ).exists()
    if slot_taken:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT,
            detail="This doctor already has an appointment at that time",
        )

    appointment = Appointment.objects.create(
        patient=patient,  # hamesha logged-in user -- request body se nahi
        doctor=doctor,
        appointment_date=when,
        reason=payload.reason.strip(),
    )
    return appointment_to_schema(appointment)


@app.post("/api/appointments/{appointment_id}/cancel", response_model=AppointmentOut)
def cancel_appointment(appointment_id: int, patient=Depends(get_patient)):
    appointment = (
        Appointment.objects.select_related("doctor")
        .filter(id=appointment_id, patient=patient)
        .first()
    )
    if appointment is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Appointment not found",
        )
    if appointment.status not in ("Pending", "Confirmed"):
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="This appointment can no longer be cancelled",
        )

    appointment.status = "Cancelled"
    appointment.save(update_fields=["status"])
    return appointment_to_schema(appointment)
