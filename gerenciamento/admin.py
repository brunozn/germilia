from django.contrib import admin
from .models import Membro, Pagamentos, FormaPagamento, PlanoFamilia, Banco, QuantidadeDiasPago


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ['cod', 'nome']


@admin.register(PlanoFamilia)
class PlanoFamiliaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    
    
@admin.register(QuantidadeDiasPago)
class QuantidadeDiasPago(admin.ModelAdmin):
    list_display = ['nome', 'quantidade_meses', 'quantidade_dias']


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'banco']


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'notas', 'status']
    list_filter = ('status',)


@admin.register(Pagamentos)
class PagamentosAdmin(admin.ModelAdmin):
    search_fields = ['membro__nome',]
    list_filter = ('membro__status', 'plano')
    list_display = ['membro', 'data_pagamento', 'notas', 'amount_paid', 'months', 'data_referente', 'debit', 'calc']
