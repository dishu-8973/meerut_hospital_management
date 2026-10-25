from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import AppointmentForm, RegisterForm
from .models import Appointment, Doctor


def home(request):
    available = Doctor.objects.filter(available=True)
    context = {
        "doctors": available.order_by("-experience")[:3],
        "doctor_count": available.count(),
        "specialty_count": available.values("specialization").distinct().count(),
    }
    return render(request, "home.html", context)


def doctor_list(request):
    available = Doctor.objects.filter(available=True)
    query = request.GET.get("q", "").strip()
    specialization = request.GET.get("specialization", "").strip()

    doctors = available
    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) | Q(specialization__icontains=query)
        )
    if specialization:
        doctors = doctors.filter(specialization=specialization)

    specializations = (
        available.values_list("specialization", flat=True)
        .distinct()
        .order_by("specialization")
    )
    return render(
        request,
        "doctors.html",
        {
            "doctors": doctors,
            "specializations": specializations,
            "query": query,
            "selected_specialization": specialization,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account ban gaya! Meerut Hospital mein aapka swagat hai.")
        return redirect("dashboard")

    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    appointments = list(
        Appointment.objects.filter(patient=request.user)
        .select_related("doctor")
        .order_by("-appointment_date")
    )
    now = timezone.now()
    upcoming = [
        a for a in appointments
        if a.status in ("Pending", "Confirmed") and a.appointment_date >= now
    ]
    completed = [a for a in appointments if a.status == "Completed"]

    return render(
        request,
        "dashboard.html",
        {
            "appointments": appointments,
            "total_count": len(appointments),
            "upcoming_count": len(upcoming),
            "completed_count": len(completed),
        },
    )


@login_required
def book_appointment(request):
    initial = {}
    doctor_id = request.GET.get("doctor", "")
    if doctor_id.isdigit():
        initial["doctor"] = int(doctor_id)

    form = AppointmentForm(request.POST or None, initial=initial)

    if request.method == "POST" and form.is_valid():
        appointment = form.save(commit=False)
        appointment.patient = request.user  # kisi aur ke naam par booking nahi ho sakti
        appointment.save()

        messages.success(request, "Appointment request submit ho gayi!")
        return redirect("dashboard")

    return render(request, "appointment_form.html", {"form": form})


@login_required
@require_POST
def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.filter(
        id=appointment_id,
        patient=request.user,
    ).first()

    if appointment is None:
        messages.error(request, "Appointment nahi mili.")
    elif appointment.status in ("Pending", "Confirmed"):
        appointment.status = "Cancelled"
        appointment.save(update_fields=["status"])
        messages.success(request, "Appointment cancel ho gayi.")
    else:
        messages.error(request, "Is appointment ko cancel nahi kiya ja sakta.")

    return redirect("dashboard")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")
