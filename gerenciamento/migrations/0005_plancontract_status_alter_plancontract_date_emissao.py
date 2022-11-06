# Generated by Django 4.1.1 on 2022-11-06 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0004_alter_plancontract_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plancontract',
            name='status',
            field=models.BooleanField(default=1),
        ),
        migrations.AlterField(
            model_name='plancontract',
            name='date_emissao',
            field=models.DateField(verbose_name='Data Emissão'),
        ),
    ]