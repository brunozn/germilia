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


# class MembroInline(admin.TabularInline):
#     fields = []


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    # fields = (('user', 'data_entrada'), ('nome', 'email'))
    fieldsets = (
        ('Dados pessoais',
         {'fields': ('user', 'data_entrada', 'nome', 'email', 'status')}),
        ('Dados complementares', {
            'fields': ('foto', 'nota')
        })
    )
    list_display = ['nome', 'nota', 'status']
    list_filter = ('status',)


@admin.register(Fatura)
class FaturaAdmin(admin.ModelAdmin):
    search_fields = ['membro__nome']
    list_filter = ('status', 'plano_familia')
    list_display = ['membro', 'data_emissao', 'data_vencimento', 'valor',
                    'tempo_plano', 'nome_fatura', 'status_fatura']
    exclude = ('nome_fatura', 'data_vencimento')
    fieldsets = (
        ('Informações membro',
         {'fields': ('membro',)}),
        ('Informações fatura',
         {'fields': (('data_emissao', 'valor'),
                     ('tempo_plano', 'plano_familia', 'status'))}),
        ('Dados complementares', {
            'fields': ('nota',)
        })

    )


@admin.register(PagamentosFatura)
class PagamentosFaturaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados pagamento',
         {'fields': ('fatura_plano', ('forma_pagamento', 'data_pagamento'))}),
        ('Dados complementares', {
            'fields': ('nota',)
        })
    )
    search_fields = ['fatura_plano__nome_fatura']
    list_display = ['fatura_plano', 'forma_pagamento', 'data_pagamento', 'nota']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['fatura_plano'].queryset = \
            Fatura.objects.filter(status__iexact='ABERTO')
        return super(PagamentosFaturaAdmin, self).render_change_form(request, context, *args, **kwargs)
