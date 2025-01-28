# Generated by Django 5.1.5 on 2025-01-24 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("brokers", "0002_currency_broker_country_broker_currency"),
        ("tickers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Inflow",
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
                ("cost_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.IntegerField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("date", models.DateField()),
                (
                    "tax",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "broker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="inflows",
                        to="brokers.broker",
                    ),
                ),
                (
                    "ticker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="inflows",
                        to="tickers.ticker",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
    ]
