from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("painel", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Solicitacao",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="quando ocorreu"
                    ),
                ),
                (
                    "requisicao",
                    models.TextField(blank=True, null=True, verbose_name="requisição"),
                ),
                (
                    "requisicao_header",
                    models.JSONField(
                        blank=True, null=True, verbose_name="cabeçalho da requisição"
                    ),
                ),
                (
                    "resposta",
                    models.TextField(blank=True, null=True, verbose_name="resposta"),
                ),
                (
                    "resposta_header",
                    models.JSONField(
                        blank=True, null=True, verbose_name="cabeçalho da resposta"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[("S", "Sucesso"), ("F", "Falha")],
                        max_length=256,
                        null=True,
                        verbose_name="status",
                    ),
                ),
                (
                    "status_code",
                    models.CharField(
                        blank=True,
                        max_length=256,
                        null=True,
                        verbose_name="status code",
                    ),
                ),
                (
                    "campus",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="painel.campus",
                    ),
                ),
                (
                    "diario",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="painel.diario",
                    ),
                ),
            ],
            options={
                "verbose_name": "solicitação",
                "verbose_name_plural": "solicitações",
                "ordering": ["-timestamp"],
            },
        ),
    ]
