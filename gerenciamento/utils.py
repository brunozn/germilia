# import os
# import tempfile
#
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.utils import timezone
# from weasyprint import HTML
#
# from gerenciamento.models import PlanContract
#
#
# def contract_export_pdf(requeste):
#     membro = requeste.user.membro
#     contratos = PlanContract.objects.filter(membro_id=membro).order_by('-date_vencimento')
#     html_string = render_to_string('reports/pdf_template.html', {'contratos': contratos})
#
#     html = HTML(string=html_string, base_url=requeste.build_absolute_uri())
#     temp_folder = tempfile.gettempdir()
#     target = os.path.join(temp_folder, 'arquivo.pdf')
#     html.write_pdf(target=target)
#
#     f = FileSystemStorage(target)
#     with f.open(target) as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="Relatorio contratos ativos.pdf"'
#         return response
