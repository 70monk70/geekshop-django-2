from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required


from common.views import CommonContextMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileEditForm
from users.models import User
from baskets.models import Basket


class UserLoginView(CommonContextMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'GeekShop - Авторизация'


class UserRegistrationView(CommonContextMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Для завершения регистрации перейдите по ссылке, направленной на Вашу почту!'
    title = 'GeekShop - Регистрация'


class UserLogoutView(LogoutView):
    pass


@login_required
@transaction.atomic
def profile(request):
    user = request.user
    if request.method == 'POST':
        edit_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        edit_form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    context = {
        'title': 'GeekShop - Профиль',
        'edit_form': edit_form,
        'profile_form': profile_form,
        'baskets': Basket.objects.filter(user=user),
    }
    return render(request, 'users/profile.html', context)

    # return HttpResponseRedirect(reverse('users:profile'))


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Поздравляем! Пользователь {user.username} активирован!')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            messages.error(request, f'Ошибка активации пользователя {user.username}')
            return HttpResponseRedirect(reverse('users:login'))
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse('users:login'))






# class UserProfileView(CommonContextMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     template_name = 'users/profile.html'
#     title = 'GeekShop - Личный кабинет'
#
#     def get_success_url(self):
#         return reverse_lazy('users:profile', args=(self.object.id,))
#
#     def get_context_data(self, **kwargs):
#         context = super(UserProfileView, self).get_context_data(**kwargs)
#         context['baskets'] = Basket.objects.filter(user=self.object)
#         return context


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'title': 'GeekShop - Авторизация', 'form': form}
#     return render(request, 'users/login.html', context)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегестрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterForm()
#     context = {'title': 'GeekShop - Регистрация', 'form': form}
#     return render(request, 'users/register.html', context)


# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=user)
#     context = {
#         'title': 'GeekShop - Личный кабинет',
#         'form': form,
#         'baskets': Basket.objects.filter(user=user),
#     }
#     return render(request, 'users/profile.html', context)
