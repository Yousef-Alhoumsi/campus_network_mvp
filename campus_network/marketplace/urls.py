from django.urls import path
from . import views

urlpatterns = [
    path("feed/",views.student_feed, name="student_feed"),
    path("apply/<int:gig_id>", views.apply_to_gig, name="apply_for_gig")
]
