# Generated by Django 3.1.3 on 2020-11-13 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0003_auto_20201112_0433'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formapagamento',
            options={'verbose_name': 'Forma Pagamento', 'verbose_name_plural': 'Formas de Pagamentos'},
        ),
        migrations.RenameField(
            model_name='membro',
            old_name='status',
            new_name='ativo',
        ),
    ]
