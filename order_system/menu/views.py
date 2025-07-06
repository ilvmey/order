from django.shortcuts import render, redirect
from .forms import OrderForm
from .sheets import append_order_to_sheet, get_restaurant_names

def order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            append_order_to_sheet(form.cleaned_data)
            return redirect('success')
    else:
        form = OrderForm()
    return render(request, 'menu/order.html', {'form': form})

def success_view(request):
    return render(request, 'menu/success.html')

def restaurant_list_view(request):
    restaurants = get_restaurant_names()
    return render(request, 'menu/restaurant_list.html', {'restaurants': restaurants})


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