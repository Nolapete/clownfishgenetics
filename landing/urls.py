from . import views
from django.urls import path

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('index/', views.index, name='index'),
    path('calculate-cross/', views.calculate_cross_htmx, name='calculate_cross_htmx'),
    path('select-parent/<int:parent_id>/', views.select_parent_htmx, name='select_parent_htmx'),
    path('filter-fish/', views.filter_fish_htmx, name='filter_fish_htmx'),
]
