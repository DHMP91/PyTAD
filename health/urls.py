from django.urls import path

from health import views
from health.api.health import HealthAPI

urlpatterns = [
    path("", views.index, name="index"),
    path("api", HealthAPI.as_view()),
]