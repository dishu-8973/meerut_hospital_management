from django.contrib import admin

from .models import Appointment, Doctor

admin.site.site_header = "Meerut Hospital Admin"
admin.site.site_title = "Meerut Hospital"
admin.site.index_title = "Hospital management"


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "experience", "available")
    list_filter = ("specialization", "available")
    list_editable = ("available",)
    search_fields = ("name", "specialization")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_date", "status")
    list_filter = ("status", "appointment_date", "doctor")
    search_fields = ("patient__username", "doctor__name")
    list_editable = ("status",)
    date_hierarchy = "appointment_date"
