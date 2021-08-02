from django.db import models
from django.db.models import Sum, FloatField, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class PlanoFamilia(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Plano'

    def __str__(self):
        return self.name


class Banco(models.Model):
    cod = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FormaPagamento(models.Model):
    name = models.CharField(max_length=50)
    banco = models.ForeignKey(Banco, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Forma Pagamento'
        verbose_name_plural = 'Formas de Pagamentos'

    def __str__(self):
        return self.name


class Membro(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    notes = models.TextField(max_length=255, null=True, blank=True)
    entry_date = models.DateTimeField()
    photo = models.ImageField(upload_to='membro_photos', null=True, blank=True)
    ativo = models.BooleanField(default=1)

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    @property
    def name_full(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Pagamentos(models.Model):
    membro = models.ForeignKey(Membro, blank=False, on_delete=models.PROTECT)
    price_month = models.DecimalField('Preço por mês', max_digits=10, decimal_places=2, default=0.00)
    months = models.IntegerField('Quant meses', default=1)
    amount_paid = models.DecimalField('Valor Pago', max_digits=5, decimal_places=2, blank=True, null=True)
    entry_date = models.DateField(default=now)
    form_pay = models.ForeignKey(FormaPagamento, null=True, blank=True, on_delete=models.CASCADE)
    plano = models.ForeignKey(PlanoFamilia, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def payable_amount(self):
        return self.price_month * self.months

    def __str__(self):
        return self.membro.name_full

    # def debit(self):
    #     return self.amount_paid - self.payable_amount()


@receiver(post_save, sender=Pagamentos)
def update_payable_amount(sender, instance, **kwargs):
    instance.amount_payable.payable_amount()

