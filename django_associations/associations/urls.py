from django.urls import path
from .views import AssociationsView

urlpatterns = [
    path('', AssociationsView.as_view(), name='associations_view'),
]
