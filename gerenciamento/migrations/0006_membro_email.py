# Generated by Django 3.2.5 on 2022-08-26 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0005_auto_20220826_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='membro',
            name='email',
            field=models.EmailField(default='email@email.com', max_length=254),
            preserve_default=False,
        ),
    ]
