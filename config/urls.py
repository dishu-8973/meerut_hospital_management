from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from hospital import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),
    path("doctors/", views.doctor_list, name="doctors"),

    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("appointments/book/", views.book_appointment, name="book_appointment"),
    path(
        "appointments/<int:appointment_id>/cancel/",
        views.cancel_appointment,
        name="cancel_appointment",
    ),
]
