import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now


class PlanoFamilia(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Plano'

    def __str__(self):
        return self.nome


class QuantidadeDiasPago(models.Model):
    nome = models.CharField(max_length=50)
    quantidade_meses = models.IntegerField('Quant meses', default=1)
    quantidade_dias = models.IntegerField('Quant dias', default=30)

    class Meta:
        verbose_name = 'Quantitativo de dias'
        verbose_name_plural = 'Quantitativo de dias'

    def __str__(self):
        return self.nome


class Banco(models.Model):
    cod = models.IntegerField(default=0, unique=True)
    nome = models.CharField(max_length=100)
    fullName = models.CharField(max_length=250)

    def __str__(self):
        return self.nome


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=50)
    banco = models.ForeignKey(
        Banco, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Forma Pagamento'
        verbose_name_plural = 'Formas de Pagamentos'

    def __str__(self):
        return self.nome


class Membro(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='membro', unique=True)
    nome = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    notas = models.TextField(max_length=255, null=True, blank=True)
    data_entrada = models.DateField()
    foto = models.ImageField(upload_to='membro_photos', null=True, blank=True)
    status = models.BooleanField(default=1)

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    def __str__(self):
        return '{}'.format(self.nome)


class Pagamentos(models.Model):
    membro = models.ForeignKey(Membro, blank=False, on_delete=models.PROTECT)
    price_month = models.DecimalField(
        'Preço por mês', max_digits=10, decimal_places=2, default=0.00)
    months = models.ForeignKey(QuantidadeDiasPago, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(
        'Valor Pago', max_digits=5, decimal_places=2, blank=True, null=True)
    data_pagamento = models.DateField('Data pagamento', default=now)
    data_referente = models.DateField('Referencia', blank=True, null=True)
    notas = models.TextField(max_length=255, null=True, blank=True)
    form_pay = models.ForeignKey(
        FormaPagamento, null=True, blank=True, on_delete=models.CASCADE)
    plano = models.ForeignKey(PlanoFamilia, null=True,
                              blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-data_pagamento',)
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return self.membro.nome

    # Débito = valor pago - valor a pagar
    def debit(self):
        history = Pagamentos.objects.filter(
            membro=self.membro, membro__status=True).order_by('data_pagamento')
        date_last = history.latest('data_pagamento').data_pagamento
        ultimo_pagamento = abs((self.data_pagamento - date_last).days)
        result = self.quantitativo(ultimo_pagamento, date_last)
        return result

    def quantitativo(self, ultimo_pagamento, date_last):
        from datetime import date
        agora = date.today()
        if ultimo_pagamento == 0:
            quant_meses = QuantidadeDiasPago.objects.filter(
                nome=self.months).last().quantidade_dias
            df = quant_meses - abs((date_last - agora).days)
            if df == 0:
                return 'Hoje é o dia: {0}'.format(df)
            elif df < 0:
                return 'Atrasado ' + str(abs(df)) + ' dias'

            return 'Restam {0} dias'.format(df)
        if ultimo_pagamento > 0:
            return 'Pago'
        return ultimo_pagamento

    def save(self, *args, **kwargs):
        self.data_referente = self.calc()
        super(Pagamentos, self).save(*args, **kwargs)

    def calc(self):
        d = Pagamentos.objects.filter(
            membro=self.membro, membro__status=True, data_pagamento=self.data_pagamento)
        if len(d) > 1:
            date_last = d.latest('data_pagamento').data_pagamento
            quantidadeMonths = d.latest('data_pagamento').months
            q2 = QuantidadeDiasPago.objects.filter(nome=quantidadeMonths)
            q = q2.first().quantidade_meses
            self.data_referente = (date_last + datetime.timedelta(q*365/12))
            return self.data_referente
        entrada = Membro.objects.get(nome=self).data_entrada
        self.data_referente = (entrada + datetime.timedelta(6*365/12))
        return self.data_referente
