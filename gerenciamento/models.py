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
    quantidade = models.IntegerField('Quant meses', default=30)

    class Meta:
        verbose_name = 'Quantitativo de dias'
        verbose_name_plural = 'Quantitativo de dias'

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
    name = models.CharField(max_length=30)
    notes = models.TextField(max_length=255, null=True, blank=True)
    entry_date = models.DateTimeField()
    photo = models.ImageField(upload_to='membro_photos', null=True, blank=True)
    ativo = models.BooleanField(default=1)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    def __str__(self):
        return '{}'.format(self.name)


class Pagamentos(models.Model):
    membro = models.ForeignKey(Membro, blank=False, on_delete=models.PROTECT)
    price_month = models.DecimalField('Preço por mês', max_digits=10, decimal_places=2, default=0.00)
    months = models.ForeignKey(QuantidadeDiasPago, on_delete=models.CASCADE)
    amount_paid = models.DecimalField('Valor Pago', max_digits=5, decimal_places=2, blank=True, null=True)
    data_pagamento = models.DateField('Data pagamento',default=now)
    form_pay = models.ForeignKey(FormaPagamento, null=True, blank=True, on_delete=models.CASCADE)
    plano = models.ForeignKey(PlanoFamilia, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-data_pagamento',)
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return self.membro.name_full

    # Débito = valor pago - valor a pagar
    def debit(self):
        history = Pagamentos.objects.filter(membro=self.membro).order_by('data_pagamento')
        date_last = history.latest('data_pagamento').data_pagamento
        ultimo_pagamento = abs((self.data_pagamento - date_last).days)
        result = self.quantitativo(ultimo_pagamento, date_last)
        return result
        
    def quantitativo(self, ultimo_pagamento, date_last, t=None):
        from datetime import date
        agora = date.today()
        if ultimo_pagamento == 0:
            quant_meses = QuantidadeDiasPago.objects.filter(name=self.months).last().quantidade
            df = quant_meses - abs((date_last - agora).days)
            if df == 0:
                return 'Hoje é o dia: {0}'.format(df)
            elif df < 0:
                return 'Atrasado ' + str(abs(df)) + ' dias'

            return 'Restam {0} dias'.format(df)
        if ultimo_pagamento > 0:
            return 'Pago'
        return ultimo_pagamento
