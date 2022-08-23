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


class QuantidadeDiasPago(models.Model):
    name = models.CharField(max_length=50)
    quant_meses = models.IntegerField('Quant meses', default=30)

    class Meta:
        verbose_name = 'Quantidade dia'

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
    months = models.ForeignKey(QuantidadeDiasPago, on_delete=models.CASCADE)
    amount_paid = models.DecimalField('Valor Pago', max_digits=5, decimal_places=2, blank=True, null=True)
    data_pagamento = models.DateField('Data pagamento',default=now)
    form_pay = models.ForeignKey(FormaPagamento, null=True, blank=True, on_delete=models.CASCADE)
    plano = models.ForeignKey(PlanoFamilia, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
    
    # quantidade pagável = preço por mes * meses
    # def payable_amount(self):
    #     return self.price_month * self.months

    def __str__(self):
        return self.membro.name_full

    # Débito = valor pago - valor a pagar
    def debit(self):
        from datetime import date
        agora = date.today()
        history = Pagamentos.objects.filter(membro=self.membro).order_by('data_pagamento')
        date_last = history.latest('data_pagamento').data_pagamento

        ultimo_pagamento = abs((self.data_pagamento - date_last).days)
        if ultimo_pagamento == 0:
            quant_meses = QuantidadeDiasPago.objects.filter(name=self.months).last().quant_meses
            df = quant_meses - abs((date_last - agora).days)
            if df == 0:
                return 'Hoje é o dia', df
            elif df < 0:
                return 'Atrasado:',  df
            return 'Restam', df
        if ultimo_pagamento > 0:
            return 'Pago'
        return ultimo_pagamento
        # debito = history2 - agora
        # return debito
        # return self.amount_paid - self.payable_amount()


# @receiver(post_save, sender=Pagamentos)
# def update_payable_amount(sender, instance, **kwargs):
#     instance.amount_payable.payable_amount()

