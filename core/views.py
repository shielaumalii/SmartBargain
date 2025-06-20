from django.shortcuts import render, redirect
from django.contrib import messages
from core.backend.login import login_user, register_user

def login_view(request):
    return render(request, "core/login.html")

def products(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request, 'core/products.html')

    
def homepage(request):
    return render(request, 'core/homepage.html')
    
def negotiate(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request, 'core/negotiate.html')


def dashboard(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request, 'core/dashboard.html')

def handle_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        success, result = login_user(email, password)

        if success:
            user = result
            request.session['username'] = user['name']
            request.session['role'] = user['role']
            request.session['email'] = user['email']
            messages.success(request, f"Welcome {user['name']} ({user['role']})")
            return redirect("homepage")
        else:
            messages.error(request, result)
            return redirect("login")

def handle_register(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("login")

        success, msg = register_user(name, email, password, role)
        if success:
            messages.success(request, msg + " Please login.")
        else:
            messages.error(request, msg)
        return redirect("login")
        
def logout_view(request):
    request.session.flush()
    return redirect("homepage")
        

