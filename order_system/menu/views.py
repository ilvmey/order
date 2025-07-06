from django.shortcuts import render, redirect
from .forms import OrderForm
from .sheets import get_restaurant_names, get_sheet_by_name

# def order_view(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             append_order_to_sheet(form.cleaned_data)
#             return redirect('success')
#     else:
#         form = OrderForm()
#     return render(request, 'menu/order.html', {'form': form})

def success_view(request):
    return render(request, 'menu/success.html')

def restaurant_list_view(request):
    restaurants = get_restaurant_names()

    menu = []
    selected_restaurant = None
    if request.method == "POST":
        selected_restaurant = request.POST.get("restaurant")
        if selected_restaurant:
            try:
                ws = get_sheet_by_name(selected_restaurant)
                menu = ws.col_values(1)
                price = ws.col_values(2)
                items = list(zip(menu, price))
            except Exception as e:
                menu = [f"⚠️ 無法讀取菜單：{e}"]

    return render(request, 'menu/restaurant_list.html', {'restaurants': restaurants, 'selected_restaurant': selected_restaurant, 'items': items})


from .sheets import append_order_to_sheet_by_restaurant

def restaurant_order_view(request, restaurant_name):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            append_order_to_sheet_by_restaurant(form.cleaned_data, restaurant_name)
            return redirect('success')
    else:
        form = OrderForm()
    return render(request, 'menu/order.html', {
        'form': form,
        'restaurant_name': restaurant_name
    })