from django import forms

from products.models import ProductCategory
from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User


class UserAdminRegisterForm(UserRegistrationForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': False}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': False}))


class ProductCategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='Скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        # fields = '__all__'
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProductCategoryEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
