from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.timezone import now
from django.dispatch import receiver
from django.contrib import admin


class TempoPlano(models.Model):
    nome = models.CharField('Nome do Plano', max_length=50)
    quantidade_meses = models.IntegerField('Quant meses', default=1)
    quantidade_dias = models.IntegerField('Quant dias', default=30)

    class Meta:
        verbose_name = 'Tempo do plano'
        verbose_name_plural = 'Tempo dos Planos'

    def __str__(self):
        return self.nome


class Banco(models.Model):
    cod_banco = models.IntegerField(default=0, unique=True)
    nome_banco = models.CharField(max_length=100)
    nome_completo_banco = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.nome_banco


class MetodoPagamento(models.Model):
    nome = models.CharField('Nome', max_length=50)
    banco = models.ForeignKey(
        Banco, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Metodo de Recebimento do Pagamento'
        verbose_name_plural = 'Metodos de Recebimento do Pagamento'

    def __str__(self):
        return self.nome


class Membro(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='membro', unique=True)
    nome = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    data_entrada = models.DateField()
    foto = models.ImageField(upload_to='membro_photos', null=True, blank=True)
    status = models.BooleanField(default=1)
    nota = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    def __str__(self):
        return '{}'.format(self.nome)


FAMILIA_CHOICES = (
    ("NETFLIX", "Netflix"),
    ("SPOTIFY", "Spotify"),
    ("NENHUM", "nenhum"),
)

STATUS_CHOICES = (
    ("ABERTO", "Aberto"),
    ("ATRASADO", "Atrasado"),
    ("PAGO", "Pago"),
)


class Fatura(models.Model):
    nome_fatura = models.CharField('Fatura', max_length=255, null=True, blank=True)
    membro = models.ForeignKey(Membro, blank=False, on_delete=models.PROTECT)
    tempo_plano = models.ForeignKey(TempoPlano, on_delete=models.CASCADE)
    valor = models.DecimalField('Valor', max_digits=5, decimal_places=2, blank=True, null=True)
    data_emissao = models.DateField('Data Emissão')
    data_vencimento = models.DateField('Vencimento', blank=True, null=True)
    nota = models.TextField('Nota', max_length=255, null=True, blank=True)
    plano_familia = models.CharField('Plano familia', max_length=9, choices=FAMILIA_CHOICES, default="NENHUM")
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="ABERTO")

    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'

    def save(self, *args, **kwargs):
        from dateutil.relativedelta import relativedelta
        self.nome_fatura = str(self.membro) + '_' + str(self.data_emissao) + '_' + str(self.plano_familia)
        self.data_vencimento = self.data_emissao + relativedelta(months=int(self.tempo_plano.quantidade_meses))
        super().save(*args, **kwargs)

    @admin.display
    def status_fatura(self):
        if self.status == "ATRASADO":
            return format_html('<span style="background: red;color: #FBFBFB">{}</span>', self.status)
        if self.status == "PAGO":
            return format_html('<span style="color: green;">{}</span>', self.status)
        return format_html('<span>{}</span>', self.status)

    def __str__(self):
        if self.nome_fatura:
            return self.nome_fatura
        return self.membro.nome


class PagamentosFatura(models.Model):
    fatura_plano = models.ForeignKey(Fatura, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(MetodoPagamento, null=True, blank=True, on_delete=models.CASCADE)
    data_pagamento = models.DateField('Data pagamento', default=now)
    nota = models.TextField('Notas', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Pagamento de Fatura'
        verbose_name_plural = 'Pagamentos dos Faturas'

    def __str__(self):
        return '{}'.format(self.fatura_plano)


@receiver(post_save, sender=PagamentosFatura)
def update_status(sender, instance, **kwargs):
    if kwargs.get('created', False):
        status = Fatura.objects.filter(pagamentosfatura=instance)
        status.update(status='PAGO')


@receiver(post_save, sender=Fatura)
def email_pay(sender, instance, **kwargs):
    if kwargs.get('created', False):
        subject = "Aviso do plano familia"
        message = render_to_string('email/email_alert_atraso.html',
                                   {'fatura': instance})
        from_email = 'brunojndias@gmail.com'
        email_payout = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[instance.membro.email],
        )
        email_payout.content_subtype = "html"
        email_payout.send()
