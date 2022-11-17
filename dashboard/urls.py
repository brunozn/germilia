from django.urls import include, path
from dashboard import views

urlpatterns = [
    path('contratos/', views.fatura_list, name='contratos_list'),
    path('pagamentos/', views.pagamentos_list, name='historic_pay'),

]
