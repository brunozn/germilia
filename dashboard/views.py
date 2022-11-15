from django.shortcuts import render

from gerenciamento.models import PlanContract, PlanContractPayment


# Create your views here.
def contrat_list(request):
    membro = request.user.membro
    contratos = PlanContract.objects.filter(membro_id=membro).order_by('-date_vencimento')
    return render(request, 'contrato_list.html', {'contratos': contratos})


def historic_pay(request):
    membro = request.user.membro
    pays = PlanContractPayment.objects.filter(contrato_plano__membro=membro)
    return render(request, 'historic_pays.html', {'pays': pays})
