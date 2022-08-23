from django.contrib import admin
from .models import Membro, Pagamentos, FormaPagamento, PlanoFamilia, Banco, QuantidadeDiasPago


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ['cod', 'name']


@admin.register(PlanoFamilia)
class PlanoFamiliaAdmin(admin.ModelAdmin):
    list_display = ['name']
    
    
@admin.register(QuantidadeDiasPago)
class QuantidadeDiasPago(admin.ModelAdmin):
    list_display = ['name', 'quant_meses']


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['name', 'banco']


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'notes', 'ativo']
    list_filter = ('ativo',)


@admin.register(Pagamentos)
class PagamentosAdmin(admin.ModelAdmin):
    list_display = ['membro', 'data_pagamento', 'amount_paid', 'months', 'plano', 'debit']
