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
    list_filter = ('membro__status', 'plan_family')
    list_display = ['membro', 'date_emissao', 'date_vencimento', 'amount', 'type_plan', 'status']


@admin.register(PlanContractPayment)
class PlanContractPaymentAdmin(admin.ModelAdmin):
    search_fields = ['contract_plan']
    list_display = ['contract_plan', 'form_pay', 'date_pay', 'note']
