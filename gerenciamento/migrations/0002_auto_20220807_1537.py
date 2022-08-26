# Generated by Django 3.2.5 on 2022-08-07 18:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuantidadeDiasPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('quant_meses', models.IntegerField(default=30, verbose_name='Quant meses')),
            ],
            options={
                'verbose_name': 'Quantidade',
            },
        ),
        migrations.RemoveField(
            model_name='pagamentos',
            name='entry_date',
        ),
        migrations.AddField(
            model_name='pagamentos',
            name='data_pagamento',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data pagamento'),
        ),
        migrations.AlterField(
            model_name='pagamentos',
            name='months',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerenciamento.quantidadediaspago'),
        ),
    ]