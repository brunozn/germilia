# Generated by Django 3.2 on 2022-11-23 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fatura',
            options={'verbose_name': 'Fatura', 'verbose_name_plural': 'Faturas'},
        ),
    ]