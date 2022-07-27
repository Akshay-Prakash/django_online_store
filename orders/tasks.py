from csv import DictWriter
from datetime import datetime, timedelta

from django.db.models import Sum

from orders.models import Order, OrderItem
from items.models import Item
from online_store.celery import app


@app.task(name="orders.tasks.generate_daily_report")
def generate_daily_report():
    today = datetime.now().strftime("%d-%b-%Y")
    daily_orders = Order.objects.filter(
        order_time__gte=(datetime.now() - timedelta(hours=24)),
        order_time__lte=datetime.now()
    )

    order_items = OrderItem.objects.filter(order__in=daily_orders)

    report = []
    report_row = {}
    total_items = 0
    total_sold_quantities = 0
    total_purchase_price = 0
    total_sell_price = 0
    total_profit_per_piece = 0
    total_profit = 0

    items = order_items.values_list('item', flat=True).distinct()

    for item_id in items:
        report_row = {}
        item = Item.objects.get(id=item_id)
        report_row = {}
        report_row["Item Name"] = item.title
        report_row["Item UPC"] = item.universal_product_code
        report_row["Sold Quantities"] = order_items.filter(
            item=item_id).aggregate(Sum('quantity'))['quantity__sum']
        report_row["Purchase Price Per Piece"] = item.purchase_price
        report_row["Sell Price Per Piece"] = item.sell_price
        report_row["Profit Per Piece"] = item.sell_price - item.purchase_price
        report_row["Total Purchase Price"] = report_row["Sold Quantities"] * \
            item.purchase_price
        report_row["Total Sell Price"] = report_row["Sold Quantities"] * \
            item.sell_price
        report_row["Total Profit"] = report_row["Sold Quantities"] * \
            report_row["Profit Per Piece"]
        # Update totals
        total_items += 1
        total_sold_quantities += report_row["Sold Quantities"]
        total_purchase_price += report_row["Total Purchase Price"]
        total_sell_price += report_row["Total Sell Price"]
        total_profit_per_piece += report_row["Profit Per Piece"]
        total_profit += report_row["Total Profit"]
        report.append(report_row)


    report_row = {}
    report_row["Item Name"] = "Totals"
    report_row["Item UPC"] = total_items
    report_row["Sold Quantities"] = total_sold_quantities
    report_row["Purchase Price Per Piece"] = ""
    report_row["Sell Price Per Piece"] = ""
    report_row["Profit Per Piece"] = total_profit_per_piece
    report_row["Total Purchase Price"] = total_purchase_price
    report_row["Total Sell Price"] = total_sold_quantities
    report_row["Total Profit"] = total_profit
    report.append(report_row)

    report_header = list(report_row.keys())

    with open(f"reports/{today}.csv", "w", newline='') as csv_file:
        dict_writer = DictWriter(csv_file, fieldnames=report_header)
        dict_writer.writeheader()
        dict_writer.writerows(report)
