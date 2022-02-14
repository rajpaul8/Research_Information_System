from django.urls import path
from . import views

urlpatterns = [
    path('', views.RISDB, name='RISDB'),
    # AJAX
    path('ajax/Load_Dependent_Sub_Region_Filters', views.Load_Dependent_Sub_Region_Filters, name='Load_Dependent_Sub_Region_Filters'),
    path('ajax/Load_Dependent_Partner_Country_Filters', views.Load_Dependent_Partner_Country_Filters, name='Load_Dependent_Partner_Country_Filters'),
]
