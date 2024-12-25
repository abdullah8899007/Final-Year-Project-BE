from flask import Flask, jsonify
from datetime import date, timedelta
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurant.settings')
django.setup()
from orders.models import Orders

app = Flask(__name__)

def get_current_month_range():
    today = date.today()
    start_of_month = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)
    end_of_month = next_month - timedelta(days=next_month.day)
    return start_of_month, end_of_month

def get_current_year_range():
    today = date.today()
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    return start_of_year, end_of_year

def get_totals(range_start, range_end):
    orders_total = {"lunch": 0, "dinner": 0}
    daily_orders_totals = {}

    orders = Orders.objects.filter(created_at__gte=range_start, created_at__lte=range_end).all()

    for order in orders:
        order_count = sum(order.items.values())
        orders_total[order.order_type.lower()] += order_count

        day = order.created_at.strftime("%Y-%m-%d")
        if day not in daily_orders_totals:
            daily_orders_totals[day] = {"lunch": 0, "dinner": 0}
        daily_orders_totals[day][order.order_type.lower()] += order_count

    return orders_total, daily_orders_totals

@app.route("/monthly-totals")
def get_monthly_totals():
    start_of_month, end_of_month = get_current_month_range()
    monthly_totals = get_totals(start_of_month, end_of_month)
    return jsonify(monthly_totals)

@app.route("/yearly-totals")
def get_yearly_totals():
    start_of_year, end_of_year = get_current_year_range()
    yearly_totals = {}

    for month in range(1, 13):
        start_of_month = start_of_year.replace(month=month)
        end_of_month = start_of_month.replace(day=28) + timedelta(days=4)
        end_of_month = end_of_month - timedelta(days=end_of_month.day)

        month_name = start_of_month.strftime("%B")
        monthly_total = get_totals(start_of_month, end_of_month)
        yearly_totals[month_name] = monthly_total

    return jsonify(yearly_totals)

if __name__ == "__main__":
    app.run(debug=True)
