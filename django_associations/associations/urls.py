from django.urls import path
from .views import AssociationsView

app_name = "associations"
urlpatterns = [
    path('', AssociationsView.as_view(), name='associations_view'),
]
