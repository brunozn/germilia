# Generated by Django 3.1.3 on 2020-11-12 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='pagamentos',
            name='form_pay',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gerenciamento.formapagamento'),
        ),
    ]
