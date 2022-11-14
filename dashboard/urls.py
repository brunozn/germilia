from django.urls import include, path
from dashboard import views


urlpatterns = [
    path('contratos/', views.contrat_list, name='contratos_list'),
]
