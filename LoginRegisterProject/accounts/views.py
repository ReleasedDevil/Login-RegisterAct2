from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages

from .forms import RegisterForm, EmailLoginForm


def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully! You can now log in."
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


class CustomLoginView(LoginView):

    template_name = 'accounts/login.html'
    authentication_form = EmailLoginForm
    redirect_authenticated_user = False

    def form_valid(self, form):

        response = super().form_valid(form)

        if self.request.POST.get('remember_me'):
            self.request.session.set_expiry(1209600)
        else:
            self.request.session.set_expiry(0)

        messages.success(
            self.request,
            "You have successfully logged in!"
        )

        return redirect('login')