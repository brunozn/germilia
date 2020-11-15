from django.db import models


class PlanoFamilia(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Plano'

    def __str__(self):
        return self.name


class FormaPagamento(models.Model):
    name = models.CharField(max_length=50)

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
    amount_payable = models.DecimalField('Valor a pagar', max_digits=5, decimal_places=2, blank=True, null=True)
    amount_paid = models.DecimalField('Valor Pago', max_digits=5, decimal_places=2, blank=True, null=True)
    membro = models.ForeignKey(Membro, blank=False, on_delete=models.PROTECT)
    form_pay = models.ForeignKey(FormaPagamento, null=True, blank=True, on_delete=models.CASCADE)
    plano = models.ForeignKey(PlanoFamilia, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    @property
    def debit(self):
        return self.amount_paid - self.amount_payable
