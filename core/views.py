from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.backend.login import login_user, register_user
from core.backend.product_manager import ProductManager
from core.backend.bargain_factory import BargainFactory

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
    return render(request, "core/negotiate.html", {
        "role": request.session.get("role", "buyer"),
    })


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
    
# Add New Product (Seller Only)
def add_product(request):
    if request.method == "POST" and request.session.get("role") == "seller":
        name = request.POST.get("name")
        image = request.POST.get("image_url")
        qty = int(request.POST.get("quantity"))
        price = float(request.POST.get("price"))
        per = request.POST.get("per")
        category = request.POST.get("category", "").lower()  # get category from form or JS
        seller_email = request.session.get("email")

        # Lookup seller_id
        from core.backend.database import create_connection
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (seller_email,))
        seller_row = cursor.fetchone()
        if not seller_row:
            return JsonResponse({"success": False, "error": "Seller not found"})
        seller_id = seller_row[0]

        ProductManager.add_product(name, image, qty, price, per, category, seller_id)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Unauthorized or bad request"})

# Edit Product (Seller Only)
def edit_product(request):
    if request.method == "POST" and request.session.get("role") == "seller":
        product_id = int(request.POST.get("product_id"))
        qty = int(request.POST.get("quantity"))
        price = float(request.POST.get("price"))
        per = request.POST.get("per")

        ProductManager.update_product(product_id, qty, price, per)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Unauthorized or bad request"})

# Delete Product (Seller Only)
def delete_product(request):
    if request.method == "POST" and request.session.get("role") == "seller":
        product_id = int(request.POST.get("product_id"))
        ProductManager.delete_product(product_id)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Unauthorized or bad request"})

# Purchase Product (Buyer Only)
def purchase_product(request):
    if request.method == "POST" and request.session.get("role") == "buyer":
        product_id = int(request.POST.get("product_id"))
        quantity = int(request.POST.get("quantity"))

        success, msg = ProductManager.purchase_product(product_id, quantity)
        return JsonResponse({"success": success, "message": msg})
    return JsonResponse({"success": False, "error": "Unauthorized or bad request"})
        
def get_products(request):
    products = ProductManager.get_all_products()
    product_list = []
    for p in products:
        product_list.append({
            "id": p[0],
            "name": p[1],
            "image": p[2],
            "qty": p[3],
            "price": p[4],
            "per": p[5],
            "category": p[6] if len(p) > 6 else "uncategorized"  # updated to pull actual category
        })
    return JsonResponse({"products": product_list})
    
def negotiate_products(request):
    products = ProductManager.get_all_products()
    product_list = []
    for p in products:
        product_list.append({
            "id": p[0],
            "name": p[1],
            "image": p[2],
            "quantity": p[3],
            "price": p[4],
            "per": p[5],
            "category": p[6]
        })
    return JsonResponse({"products": product_list})

@csrf_exempt
def save_bargain_setting(request):
    if request.method == "POST":
        data = json.loads(request.body)
        setting = BargainFactory.create_setting(
            data["product_id"], data["min_quantity"], data["min_price"]
        )
        setting.save()
        return JsonResponse({"status": "success"})

@csrf_exempt
def save_bargain_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Use session or dummy user_id for now
        user_id = request.session.get("user_id", 1)
        req = BargainFactory.create_request(
            data["product_id"], user_id, data["quantity"], data["price"]
        )
        req.save()
        return JsonResponse({"status": "success"})