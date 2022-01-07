from django.contrib.auth.decorators import login_required
from .models import User
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string

# Create your views here.
from user_authentication.forms import NewUserForm, UserForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
import datetime


def register_user(request):
    if request.method == "POST":
        context = {}
        context["username"] = request.POST.get('username')
        context["first_name"] = request.POST.get('first_name')
        context["last_name"] = request.POST.get('last_name')
        context["email"] = request.POST.get('email')
        context["password"] = make_password(request.POST.get('password'))
        context["password_confirmation"] = make_password(request.POST.get('password_confirmation'))
        context['date_joined'] = datetime.datetime.now().date()
        context['is_active'] = True

        form = NewUserForm(context)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "register.html", {"form": form})


@login_required(login_url='/login')
def home(request):
    context = {"users": User.objects.all()}
    return render(request, "home.html", context)


def login_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        if user is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.login_attempt <= 3:
                    login(request, user)
                    user.login_attempt = 0
                    user.save()
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("/")
                else:
                    messages.error(request, "You are exceeded maximum login attempt")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('/login')


def destroy_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/")


@login_required(login_url='/login')
def new_user(request):
    if request.method == "POST":
        context = {}
        context["username"] = request.POST.get('username')
        context["first_name"] = request.POST.get('first_name')
        context["last_name"] = request.POST.get('last_name')
        context["email"] = request.POST.get('email')
        context["password"] = make_password(request.POST.get('password'))
        context["password_confirmation"] = make_password(request.POST.get('password_confirmation'))
        context['date_joined'] = datetime.datetime.now().date()
        context['is_active'] = True

        form = NewUserForm(context)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User created successfully.")
            return redirect("/")
        messages.error(request, "Invalid information.")
    form = NewUserForm()
    return render(request, "new_user.html", {"form": form})


@login_required(login_url='/login')
def edit(request, id):
    user = User.objects.get(id=id)
    return render(request, 'edit_user.html', {'user': user})


@login_required(login_url='/login')
def update(request, id):
    user = User.objects.get(id=id)
    form = UserForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, 'edit_user.html', {'user': user})


def forgot_password(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST.get('email'))
            msg_html = render_to_string('email.html', {'user': user})
            send_mail("Reset Password", 't',
                      "gopalakrishnankishore510@gmail.com", [user.email], html_message=msg_html)
            return redirect("/login")
        except User.DoesNotExist:
            return redirect("/login")
    return render(request, 'forgot_password.html')


def new_passwords(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST.get('email'))
            user.password = make_password(request.POST.get("password"))
            user.save()
            return redirect("/login")
        except User.DoesNotExist:
            return redirect("/login")
    return render(request, "new_password.html", { 'email': request.GET.get("email") })