from django.contrib import admin
from django.urls import include, path

from home.views import index, sair, login_membro
from germilia.views import pdf_contrat_view, pdf_pay_view
from django.conf import settings
from django.conf.urls.static import static
# from germilia.germilia import settings

urlpatterns = [
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login_membro, name='login'),
    path('sair/', sair, name='sair'),
    path('pdf/', pdf_contrat_view, name='pdf_fatura'),
    path('pay/pdf/', pdf_pay_view, name='pdf_pay'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Gerenciador de familias'
admin.site.index_title = 'Germilia'
admin.site.site_title = 'Seja bem vindo ao Germilia'
