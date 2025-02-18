from django.urls import path
from .views import confirm_attendance


urlpatterns=[
    path("attendance/confirm/", confirm_attendance, name="confirm_attendance")
]