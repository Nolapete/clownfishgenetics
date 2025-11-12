from django.urls import path

from . import views

# Import specific views if preferred over using views. prefix
# from .views import VarietyListView, ...

urlpatterns = [
    # Variety URLs
    path("varieties/", views.VarietyListView.as_view(), name="variety-list"),
    path("varieties/new/", views.VarietyCreateView.as_view(), name="variety-create"),
    path(
        "varieties/<int:pk>/", views.VarietyDetailView.as_view(), name="variety-detail"
    ),
    # Parent URLs
    path("parents/", views.ParentListView.as_view(), name="parent-list"),
    path("parents/<int:pk>/", views.ParentDetailView.as_view(), name="parent-detail"),
    path("parents/new/", views.ParentCreateView.as_view(), name="parent-create"),
    # Cross URLs
    path("crosses/", views.CrossListView.as_view(), name="cross-list"),
    path("crosses/new/", views.CrossCreateView.as_view(), name="cross-create"),
    path("crosses/<int:pk>/", views.CrossDetailView.as_view(), name="cross-detail"),
    path(
        "crosses/<int:cross_id>/calculate/",
        views.calculate_cross_results,
        name="cross-calculate",
    ),
    # Basic App Index
    path("", views.CrossListView.as_view(), name="index"),
]
