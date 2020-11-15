from django.contrib import admin
from .models import Membro, Pagamentos, FormaPagamento, PlanoFamilia


@admin.register(PlanoFamilia)
class PlanoFamiliaAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'notes', 'ativo']


@admin.register(Pagamentos)
class PagamentosAdmin(admin.ModelAdmin):
    list_display = ['membro', 'amount_payable', 'amount_paid', 'debit', 'plano']
