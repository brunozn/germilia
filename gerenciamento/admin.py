from django.contrib import admin
from .models import Membro, Fatura, Banco, MetodoPagamento, TempoPlano, PagamentosFatura


@admin.register(Banco)
class BankAdmin(admin.ModelAdmin):
    list_display = ['nome_banco', 'cod_banco']

    
@admin.register(TempoPlano)
class TempoPlanoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade_meses', 'quantidade_dias']


@admin.register(MetodoPagamento)
class MetodoPagamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'banco']


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'nota', 'status']
    list_filter = ('status',)


@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_filter = ('status', 'plano_familia')
    list_display = ['membro', 'data_emissao', 'data_vencimento', 'valor',
                    'tempo_plano', 'nome_fatura', 'status_fatura']


@admin.register(PagamentosFatura)
class PagamentosFaturaAdmin(admin.ModelAdmin):
    search_fields = ['fatura_plano']
    list_display = ['fatura_plano', 'forma_pagamento', 'data_pagamento', 'nota']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['fatura_plano'].queryset = \
            Fatura.objects.filter(status__iexact='ABERTO')
        return super(PagamentosFatura, self).render_change_form(request, context, *args, **kwargs)
