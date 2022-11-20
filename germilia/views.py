import os
import tempfile

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from gerenciamento.models import Fatura, PagamentosFatura


def pdf_fatura_view(request):
    membro = request.user.membro
    faturas = Fatura.objects.filter(membro_id=membro).order_by('-data_vencimento')
    html_string = render_to_string('reports/pdf_template.html', {'faturas': faturas})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    temp_folder = tempfile.gettempdir()
    target = os.path.join(temp_folder, 'file.pdf')
    html.write_pdf(target=target)

    f = FileSystemStorage(target)
    with f.open(target) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Relatorio_Faturas.pdf"'
        return response


def pdf_pagamentos_view(request):
    pagamentos = PagamentosFatura.objects.filter(fatura_plano__membro=request.user.membro).order_by('-data_pagamento')
    html_string = render_to_string('reports/pdf_pagamentos_template.html', {'pagamentos': pagamentos})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    temp_folder = tempfile.gettempdir()
    target = os.path.join(temp_folder, 'arquivo.pdf')
    html.write_pdf(target=target)

    f = FileSystemStorage(target)
    with f.open(target) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Relatorio faturas.pdf"'
        return response

