from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gerenciamento.models import Fatura, PagamentosFatura


@login_required(login_url='/login/')
def fatura_list(request):
    membro = request.user.membro
    faturas = Fatura.objects.filter(membro_id=membro).order_by('-date_vencimento')
    return render(request, 'fatura_list.html', {'faturas': faturas})


@login_required(login_url='/login/')
def pagamentos_list(request):
    membro = request.user.membro
    pagamentos = PagamentosFatura.objects.filter(fatura_plano__membro=membro)
    return render(request, 'pagamentos_list.html', {'pagamentos': pagamentos})
