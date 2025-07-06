from collections import defaultdict, Counter
from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.urls import reverse
from .sheets import get_restaurant_names, get_sheet_by_name, read_orders_from_sheet, write_orders_to_sheet


def restaurant_list_view(request):
    restaurants = get_restaurant_names()
    order_seats = ['老師'] + [str(i) for i in range(1, 21) if i != 8]

    selected_restaurant = request.POST.get("restaurant") if request.method == "POST" else request.GET.get("restaurant")

    items = []
    if selected_restaurant:
        try:
            ws = get_sheet_by_name(selected_restaurant)
            menu = ws.col_values(1)
            price = ws.col_values(2)
            items = list(zip(menu, price))
        except Exception as e:
            items = [(f"⚠️ 無法讀取菜單：{e}", "")]

    orders = []
    selected_meals = {}
    meal_counter = defaultdict(int)
    seat_total = defaultdict(int)
    total_price = 0
    seat_meal_detail = defaultdict(list)

    if request.method == "POST":
        for seat in order_seats:
            meals = request.POST.getlist(f"meal_{seat}[]")
            if meals:
                selected_meals[seat] = meals
                for meal in meals:
                    meal_price = next((int(p) for n, p in items if n == meal), 0)
                    orders.append((seat, meal, meal_price))

        if orders:
            write_orders_to_sheet(orders)
        query_string = urlencode({'restaurant': selected_restaurant})
        return redirect(f"{reverse('restaurant_list')}?{query_string}")

    latest_orders = read_orders_from_sheet()
    for seat, meal, price in latest_orders:
        meal_counter[meal] += 1
        seat_total[seat] += price
        total_price += price
        seat_meal_detail[seat].append((meal, price))

    seat_detail_summary = {}
    for seat, meals in seat_meal_detail.items():
        # 用 Counter 統計同一個餐點被點幾次
        meal_summary = Counter(meals)
        seat_detail_summary[seat] = {
            'items': [(f"{meal} × {count}", price * count) for (meal, price), count in meal_summary.items()],
            'total': seat_total[seat]
        }

    return render(request, 'menu/restaurant_list.html', {
        'restaurants': restaurants,
        'selected_restaurant': selected_restaurant,
        'items': items,
        'order_seats': order_seats,
        'selected_meals': selected_meals,
        'orders': orders,
        'meal_counter': dict(meal_counter),
        'seat_total': dict(seat_total),
        'total_price': total_price,
        'seat_detail_summary': seat_detail_summary,
    })
