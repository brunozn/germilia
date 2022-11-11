from django.contrib import admin
from .models import Membro, PlanContract, Bank, PaymentMethod, TypePlan, PlanContractPayment


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['nameBank', 'codBank']

    
@admin.register(TypePlan)
class TypePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantidade_meses', 'quantidade_dias']


@admin.register(PaymentMethod)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['name', 'bank']


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ['name', 'note', 'status']
    list_filter = ('status',)


@admin.register(PlanContract)
class PlanAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('status', 'plan_family')
    list_display = ['membro', 'date_emissao', 'date_vencimento', 'amount',
                    'tipo_plano', 'nome_contrato', 'status_contrato']


@admin.register(PlanContractPayment)
class PlanContractPaymentAdmin(admin.ModelAdmin):
    search_fields = ['contrato_plano']
    list_display = ['contrato_plano', 'forma_pagamento', 'data_pagamento', 'nota']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['contrato_plano'].queryset = \
            PlanContract.objects.filter(status__iexact='ABERTO')
        return super(PlanContractPaymentAdmin, self).render_change_form(request, context, *args, **kwargs)
