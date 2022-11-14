from django.shortcuts import render

from gerenciamento.models import PlanContract


# Create your views here.
def contrat_list(request):
    membro = request.user.membro
    contratos = PlanContract.objects.filter(membro_id=membro).order_by('-date_vencimento')
    return render(request, 'contrato_list.html', {'contratos': contratos})
