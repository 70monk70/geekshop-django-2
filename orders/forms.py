from django import forms
from orders.models import Order, OrderItem
from products.models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)


def __init__(self, *args, **kwargs):
    super(OrderForm, self).__init__(*args, **kwargs)
    for field_name, field in self.fields.items():
        field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='Цена за единицу', required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.get_items()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
