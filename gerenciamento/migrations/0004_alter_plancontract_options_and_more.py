# Generated by Django 4.1.1 on 2022-11-06 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0003_plancontract_delete_plan'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plancontract',
            options={'verbose_name': 'Contrato do Plano', 'verbose_name_plural': 'Contratos dos Planos'},
        ),
        migrations.RemoveField(
            model_name='plancontract',
            name='form_pay',
        ),
        migrations.AlterField(
            model_name='plancontract',
            name='date_emissao',
            field=models.DateField(verbose_name='Data pagamento'),
        ),
    ]