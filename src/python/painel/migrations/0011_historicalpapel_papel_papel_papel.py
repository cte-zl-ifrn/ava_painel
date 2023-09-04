# Generated by Django 4.2.4 on 2023-08-23 20:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("painel", "0010_cursopolo_campus_historicalcursopolo_campus_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalpapel",
            name="papel",
            field=models.CharField(
                db_index=True, default="teacher", max_length=10, verbose_name="papel"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="papel",
            name="papel",
            field=models.CharField(
                default="teacher", max_length=10, unique=True, verbose_name="papel"
            ),
            preserve_default=False,
        ),
    ]