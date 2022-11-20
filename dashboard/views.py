from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from gerenciamento.models import Fatura, PagamentosFatura
from django.core.paginator import Paginator, EmptyPage, InvalidPage


@login_required(login_url='/login/')
def fatura_list(request):
    membro = request.user.membro
    faturas = Fatura.objects.filter(membro_id=membro).order_by('-data_vencimento')
    paginator = Paginator(faturas, 6)
    page = int(request.GET.get('page', '1'))
    try:
        faturas = paginator.page(page)
    except (EmptyPage, InvalidPage):
        faturas = paginator.page(paginator.num_pages)
    return render(request, 'fatura_list.html', {'faturas': faturas})


@login_required(login_url='/login/')
def pagamentos_list(request):
    pagamentos = PagamentosFatura.objects.filter(fatura_plano__membro=request.user.membro)
    paginator = Paginator(pagamentos, 6)
    page = int(request.GET.get('page', '1'))
    try:
        pagamentos = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pagamentos = paginator.page(paginator.num_pages)
    return render(request, 'pagamentos_list.html', {'pagamentos': pagamentos})


@login_required(login_url='/login/')
def painel(request):
    membro = request.user.membro
    pagamentos = PagamentosFatura.objects.filter(fatura_plano__membro=membro)[:3]
    faturas = Fatura.objects.filter(membro_id=membro).order_by('-data_vencimento')[:3]
    return render(request, 'painel.html', {'pagamentos': pagamentos, 'faturas': faturas, 'membro': membro})
