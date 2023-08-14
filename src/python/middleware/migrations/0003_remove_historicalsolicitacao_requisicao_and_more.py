# Generated by Django 4.2.4 on 2023-08-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "middleware",
            "0002_solicitacao_deleted_solicitacao_deleted_by_cascade_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalsolicitacao",
            name="requisicao",
        ),
        migrations.RemoveField(
            model_name="historicalsolicitacao",
            name="requisicao_header",
        ),
        migrations.RemoveField(
            model_name="historicalsolicitacao",
            name="resposta",
        ),
        migrations.RemoveField(
            model_name="historicalsolicitacao",
            name="resposta_header",
        ),
        migrations.RemoveField(
            model_name="solicitacao",
            name="requisicao",
        ),
        migrations.RemoveField(
            model_name="solicitacao",
            name="requisicao_header",
        ),
        migrations.RemoveField(
            model_name="solicitacao",
            name="resposta",
        ),
        migrations.RemoveField(
            model_name="solicitacao",
            name="resposta_header",
        ),
        migrations.AddField(
            model_name="historicalsolicitacao",
            name="enviado",
            field=models.TextField(blank=True, null=True, verbose_name="JSON enviado"),
        ),
        migrations.AddField(
            model_name="historicalsolicitacao",
            name="recebido",
            field=models.TextField(blank=True, null=True, verbose_name="JSON recebido"),
        ),
        migrations.AddField(
            model_name="historicalsolicitacao",
            name="respondido",
            field=models.TextField(
                blank=True, null=True, verbose_name="JSON respondido"
            ),
        ),
        migrations.AddField(
            model_name="solicitacao",
            name="enviado",
            field=models.TextField(blank=True, null=True, verbose_name="JSON enviado"),
        ),
        migrations.AddField(
            model_name="solicitacao",
            name="recebido",
            field=models.TextField(blank=True, null=True, verbose_name="JSON recebido"),
        ),
        migrations.AddField(
            model_name="solicitacao",
            name="respondido",
            field=models.TextField(
                blank=True, null=True, verbose_name="JSON respondido"
            ),
        ),
        migrations.AlterField(
            model_name="historicalsolicitacao",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("S", "Sucesso"), ("F", "Falha"), ("P", "Processando")],
                max_length=256,
                null=True,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="solicitacao",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("S", "Sucesso"), ("F", "Falha"), ("P", "Processando")],
                max_length=256,
                null=True,
                verbose_name="status",
            ),
        ),
    ]