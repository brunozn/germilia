from django.contrib import admin
from .models import Membro, Pagamentos, FormaPagamento, PlanoFamilia, Banco


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ['cod', 'name']


@admin.register(PlanoFamilia)
class PlanoFamiliaAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['name', 'banco']


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'notes', 'ativo']
    list_filter = ('ativo',)


@admin.register(Pagamentos)
class PagamentosAdmin(admin.ModelAdmin):
    list_display = ['membro', 'payable_amount', 'amount_paid', 'plano']
