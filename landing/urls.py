from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("index/", views.index, name="index"),
    path("cbr/", views.cbr, name="cbr"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("calculate-cross/", views.calculate_cross_htmx, name="calculate_cross_htmx"),
    path(
        "select-parent/<int:parent_id>/",
        views.select_parent_htmx,
        name="select_parent_htmx",
    ),
    path("filter-fish/", views.filter_fish_htmx, name="filter_fish_htmx"),
]
