# Generated by Django 5.1.5 on 2025-01-31 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inflows", "0002_alter_inflow_total_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="inflow",
            name="type",
            field=models.CharField(
                choices=[("Compra", "Compra"), ("Subscrição", "Subscrição")],
                default="Compras",
                max_length=20,
            ),
        ),
    ]
