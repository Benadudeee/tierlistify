from django.shortcuts import render, redirect
from django.http import HttpResponse

from main.views import get_user_or_anon
from .forms import LoginForm, UserRegistrationForm
from .tokens import account_activation_token

from django.utils.encoding import smart_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model

from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.
def login(request):
    user_or_anonymous = get_user_or_anon(request.user)

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # NOTE: You could use the all funtion to see if multiple variables have values
            if all ([username, password]):
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    auth_login(request, user)
                    return redirect("/")

    form = LoginForm() 

    data = {
        "user" : user_or_anonymous,
        "form" : form
    }
    return render(request, 'auth/login.html', data)

def logout(request):
    auth_logout(request)

    return redirect("/")

def register(request):
    user_or_anonymous = get_user_or_anon(request.user)

    if request.method == "POST":
        # Gets the POST data from UserRegistrationForm
        form = UserRegistrationForm(request.POST)

        # If ALL fields are properly inputted
        if form.is_valid():
            # Save all user data and loggs the the user in
            user = form.save()
            user.is_active = False

            return email_send_view(request, user)
        else: # Otherwise, something went wrong and the form will return with errors
            data = {
                "form": form,
                "user" : user_or_anonymous
            }
            return render(request, "auth/register.html", data)
        
    # Displays the form to the user when they click on the page
    form = UserRegistrationForm()
    data = {
        "form" : form,
        "user" : user_or_anonymous
    }
    return render(request, "auth/register.html", data)


def email_send_view(request, user):
    mail_subject = f"Account creation for ${user.email}"

    data = {
        'user' : user,
        'domain' : get_current_site(request).domain,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token' : account_activation_token.make_token(user)
    }
    message = render_to_string('auth/account_activation_email.html', data)

    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()

    return render(request, "auth/email_check.html")

def activate(request, uidb64, token):
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        # return redirect('home')
        return render(request, 'auth/email_success.html')
    else:
        return HttpResponse('Activation link is invalid!')