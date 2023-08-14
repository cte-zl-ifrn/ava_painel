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
        migrations.RenameField("historicalsolicitacao", "requisicao", "recebido"),
        migrations.RemoveField(
            model_name="historicalsolicitacao",
            name="requisicao_header",
        ),
        migrations.RenameField("historicalsolicitacao", "resposta", "respondido"),
        migrations.RemoveField(
            model_name="historicalsolicitacao",
            name="resposta_header",
        ),
        migrations.RenameField("solicitacao", "requisicao", "recebido"),
        migrations.RemoveField(
            model_name="solicitacao",
            name="requisicao_header",
        ),
        migrations.RenameField("solicitacao", "resposta", "respondido"),
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
            model_name="solicitacao",
            name="enviado",
            field=models.TextField(blank=True, null=True, verbose_name="JSON enviado"),
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
