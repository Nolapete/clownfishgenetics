from django.urls import path

from . import views

urlpatterns = [
    path("", views.calculator_view, name="calculator_view"),
    path("parent-selection/", views.parent_selection_view, name="parent_selection"),
]
