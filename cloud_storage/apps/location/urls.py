from django.urls import path
from apps.location.views import LocationView

urlpatterns = [
    path('location/', LocationView.as_view(), name='location'),
]