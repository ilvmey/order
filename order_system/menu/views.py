from collections import defaultdict
from django.shortcuts import render, redirect
from .forms import OrderForm
from .sheets import get_restaurant_names, get_sheet_by_name, write_orders_to_sheet


def success_view(request):
    return render(request, 'menu/success.html')

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

    if request.method == "POST":
        for seat in order_seats:
            meals = request.POST.getlist(f"meal_{seat}[]")
            if meals:
                selected_meals[seat] = meals
                for meal in meals:
                    meal_price = next((int(p) for n, p in items if n == meal), 0)
                    orders.append((seat, meal, meal_price))
                    meal_counter[meal] += 1
                    seat_total[seat] += meal_price
                    total_price += meal_price

        if orders:
            write_orders_to_sheet(orders)

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
    })




# from .sheets import append_order_to_sheet_by_restaurant

# def restaurant_order_view(request, restaurant_name):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             append_order_to_sheet_by_restaurant(form.cleaned_data, restaurant_name)
#             return redirect('success')
#     else:
#         form = OrderForm()
#     return render(request, 'menu/order.html', {
#         'form': form,
#         'restaurant_name': restaurant_name
#     })