from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.timezone import now
from django.dispatch import receiver
from django.contrib import admin


class TypePlan(models.Model):
    name = models.CharField('Nome do Plano', max_length=50)
    quantidade_meses = models.IntegerField('Quant meses', default=1)
    quantidade_dias = models.IntegerField('Quant dias', default=30)

    class Meta:
        verbose_name = 'Tipos de Planos'
        verbose_name_plural = 'Tipos de Planos'

    def __str__(self):
        return self.name


class Bank(models.Model):
    codBank = models.IntegerField('Codigo', default=0, unique=True)
    nameBank = models.CharField('Nome', max_length=100)
    fullName = models.CharField('Nome Completo', max_length=250)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.nameBank


class PaymentMethod(models.Model):
    name = models.CharField('Nome', max_length=50)
    bank = models.ForeignKey(
        Bank, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Metodo de Recebimento do Pagamento'
        verbose_name_plural = 'Metodos de Recebimento do Pagamento'

    def __str__(self):
        return self.name


class Membro(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='membro', unique=True)
    name = models.CharField('Nome', max_length=30)
    email = models.EmailField(max_length=254)
    data_entrada = models.DateField()
    foto = models.ImageField(upload_to='membro_photos', null=True, blank=True)
    status = models.BooleanField(default=1)
    note = models.TextField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    def __str__(self):
        return '{}'.format(self.name)


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


class PlanContract(models.Model):
    nome_contrato = models.CharField('Nome do contrato', max_length=255, null=True, blank=True)
    membro = models.ForeignKey(Membro, blank=False, on_delete=models.PROTECT)
    tipo_plano = models.ForeignKey(TypePlan, on_delete=models.CASCADE)
    amount = models.DecimalField('Valor', max_digits=5, decimal_places=2, blank=True, null=True)
    date_emissao = models.DateField('Data Emissão')
    date_vencimento = models.DateField('Vencimento', blank=True, null=True)
    note = models.TextField('Nota', max_length=255, null=True, blank=True)
    plan_family = models.CharField('Plano familia', max_length=9, choices=FAMILIA_CHOICES, default="NENHUM")
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="ABERTO")

    class Meta:
        verbose_name = 'Contrato do Plano'
        verbose_name_plural = 'Contratos dos Planos'

    def save(self, *args, **kwargs):
        self.nome_contrato = str(self.membro) + '_' + str(self.date_emissao) + '_' + str(self.plan_family)
        super().save(*args, **kwargs)

    @admin.display
    def status_contrato(self):
        if self.status == "ATRASADO":
            return format_html('<span style="background: red;color: #FBFBFB">{}</span>', self.status)
        if self.status == "PAGO":
            return format_html('<span style="color: green;">{}</span>', self.status)
        return format_html('<span>{}</span>', self.status)

    def __str__(self):
        if self.nome_contrato:
            return self.nome_contrato
        return self.membro.name


class PlanContractPayment(models.Model):
    contrato_plano = models.ForeignKey(PlanContract, on_delete=models.CASCADE)
    forma_pagamento = models.ForeignKey(PaymentMethod, null=True, blank=True, on_delete=models.CASCADE)
    data_pagamento = models.DateField('Data pagamento', default=now)
    nota = models.TextField('Notas', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Pagamento de Contrato'
        verbose_name_plural = 'Pagamentos dos Contratos'

    def __str__(self):
        return '{}'.format(self.contrato_plano)


@receiver(post_save, sender=PlanContractPayment)
def update_status(sender, instance, **kwargs):
    if kwargs.get('created', False):
        status = PlanContract.objects.filter(plancontractpayment=instance)
        status.update(status='PAGO')


@receiver(post_save, sender=PlanContract)
def email_pay(sender, instance, **kwargs):
    if kwargs.get('created', False):
        subject = "Aviso do plano familia"
        message = render_to_string('email/email_alert_atraso.html',
                                   {'contrato': instance})
        from_email = 'brunojndias@gmail.com'
        email_payout = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[instance.membro.email],
        )
        email_payout.content_subtype = "html"
        email_payout.send()
