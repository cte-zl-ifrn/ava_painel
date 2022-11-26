# Generated by Django 4.1.3 on 2022-11-25 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_ambiente_cor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambiente',
            name='cor',
            field=models.CharField(help_text="Escolha uma cor em RGB. Ex.: <span style='background: #a154d0; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#a154d0</span> <span style='background: #438f4b; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#438f4b</span> <span style='background: #c90c0f; color: #fff; padding: 1px 5px; font-size: 95%; border-radius: 4px;'>#c90c0f</span>", max_length=255, verbose_name='cor do ambiente'),
        ),
        migrations.AlterField(
            model_name='ambiente',
            name='sigla',
            field=models.CharField(help_text='Esta é a sigla que vai aparecer no dashboard', max_length=255, unique=True, verbose_name='sigla do ambiente'),
        ),
    ]
