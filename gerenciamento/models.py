from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.dispatch import receiver


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
        verbose_name = 'Forma Pagamento'
        verbose_name_plural = 'Formas de Pagamentos'

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
    ("EMDIA", "Em dia"),
    ("ATRASADO", "Atrasado"),
    ("NENHUM", "nenhum"),
)


class PlanContract(models.Model):
    membro = models.ForeignKey(Membro, blank=False, on_delete=models.PROTECT)
    type_plan = models.ForeignKey(TypePlan, on_delete=models.CASCADE)
    amount = models.DecimalField('Valor', max_digits=5, decimal_places=2, blank=True, null=True)
    date_emissao = models.DateField('Data Emissão')
    date_vencimento = models.DateField('Vencimento', blank=True, null=True)
    note = models.TextField('Nota', max_length=255, null=True, blank=True)
    plan_family = models.CharField('plano familia', max_length=9, choices=FAMILIA_CHOICES, default="NENHUM")
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="ABERTO")

    class Meta:
        verbose_name = 'Contrato do Plano'
        verbose_name_plural = 'Contratos dos Planos'

    def __str__(self):
        return self.membro.name


class PlanContractPayment(models.Model):
    contract_plan = models.ForeignKey(PlanContract, on_delete=models.CASCADE)
    form_pay = models.ForeignKey(PaymentMethod, null=True, blank=True, on_delete=models.CASCADE)
    date_pay = models.DateField('Data pagamento', default=now)
    note = models.TextField('Notas', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Pagamento de Contrato'
        verbose_name_plural = 'Pagamentos dos Contratos'

    def __str__(self):
        return '{}'.format(self.contract_plan)


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
