# menu/forms.py
from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(label='姓名')
    item = forms.ChoiceField(label='餐點', choices=[
        ('飯', '飯'),
        ('麵', '麵'),
        ('飲料', '飲料'),
    ])
    quantity = forms.IntegerField(label='數量', min_value=1)
