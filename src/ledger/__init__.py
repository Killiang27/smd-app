import csv
import sys
from decimal import Decimal
from pathlib import Path

from rich.console import Console
from rich.table import Table

DATA = Path("data/transactions.csv")


def read_rows(path: Path = DATA) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def totals_by(rows: list[dict[str, str]], key: str) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = {}
    for row in rows:
        totals[row[key]] = totals.get(row[key], Decimal(0)) + Decimal(row["amount"])
    return totals


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else "balance"
    rows = read_rows()
    if command == "balance":
        for account, total in sorted(totals_by(rows, "account").items()):
            print(f"{account} {total:.2f}")
    elif command == "spending":
        outgoing = [
            row
            for row in rows
            if row["category"] != "transfer" and Decimal(row["amount"]) < 0
        ]
        spending = totals_by(outgoing, "category")
        table = Table(title="Spending by category")
        table.add_column("Category")
        table.add_column("Total", justify="right")
        for category, total in sorted(spending.items(), key=lambda item: item[1]):
            table.add_row(category, f"{total:.2f}")
        Console().print(table)
    else:
        sys.exit(f"unknown command: {command}")
