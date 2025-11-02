from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "clownfishgenetics.org Administration"
admin.site.site_title = "clownfishgenetics.org"
admin.site.index_title = "Clownfish Genetics Admin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('calculator/', include('calculator.urls')),
    path('breeding/', include('calcRefactor.urls')),
]
