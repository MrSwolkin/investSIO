import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from brokers.models import Broker
from inflows.models import Inflow
from outflows.models import Outflow
from tickers.models import Ticker

class Command(BaseCommand):
    help = "create a new transaction."
    
    def add_arguments(self, parser):
        parser.add_argument("file_name", type=str, help="nome do arquivo com Fiis")
    
    def handle(self, *args, **options):
        print(f"Argumento recebido {options}")
        file_name = options["file_name"]

        with open(file_name, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
                ticker = row.get("ticker").upper()
                date = row.get("date")
                type = row.get("type").lower()
                quantity = int(row.get("quantity", 0))
                cost_price = float(row.get("cost_price", 0))
                broker_name = row.get("broker", None)
                try:
                    # Convertendo a data para YYYY-MM-DD
                    date = datetime.strptime(date, "%d/%m/%Y").date()

                    ticker = Ticker.objects.get(name=ticker)
                    broker = Broker.objects.get(name=broker_name) if broker_name else None
                    
                    if type in ["compra", "subscrição"]:
                        Inflow.objects.create(
                            ticker=ticker,
                            date=date,
                            type=type,
                            quantity=(quantity),
                            broker=broker,
                            cost_price=(cost_price),
                        )
                    elif type == "venda":
                        Outflow.objects.create(
                            ticker=ticker,
                            date=date,
                            
                            quantity=quantity,
                            broker=broker,
                            cost_price=cost_price,
                        )
                    self.stdout.write(self.style.SUCCESS(f"Transação de {ticker} ({type} importada)"))
                    
                except Ticker.DoesNotExist:
                    self.stderr.write(self.style.ERROR(
                        f"Ticker '{ticker}' não encontrado."))
                except Broker.DoesNotExist:
                    self.stderr.write(self.style.ERROR(
                        f"Corretora '{broker}' não encontrada."))
        self.stdout.write(self.style.SUCCESS("Conlcuido"))
