from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.backend.login import login_user, register_user
from core.backend.product_manager import ProductManager
from core.backend.bargain_factory import BargainFactory
from core.backend.database import create_connection
from core.backend.dashboard import get_orders_for_user
from core.backend.dashboard import get_negotiation_tasks
from core.backend.dashboard import save_negotiation_response
from core.backend.dashboard import get_negotiation_dashboard_data
from core.backend.dashboard import update_negotiation_dashboard_response 

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
    return render(request, 'core/dashboard.html', {
        "email": request.session.get("email"),
        "role": request.session.get("role")
    })

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
            request.session['user_id'] = user['id']
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
        unit = request.POST.get('unit', 'kg')
        category = request.POST.get("category", "").lower()
        seller_email = request.session.get("email")

        from core.backend.database import create_connection
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (seller_email,))
        seller_row = cursor.fetchone()
        if not seller_row:
            return JsonResponse({"success": False, "error": "Seller not found"})
        seller_id = seller_row[0]

        ProductManager.add_product(name, image, qty, price, per, unit, category, seller_id)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Unauthorized or bad request"})

# Edit Product (Seller Only) — FIXED TO INCLUDE UNIT
def edit_product(request):
    if request.method == "POST" and request.session.get("role") == "seller":
        product_id = int(request.POST.get("product_id"))
        qty = int(request.POST.get("quantity"))
        price = float(request.POST.get("price"))
        per = request.POST.get("per")
        unit = request.POST.get("unit")

        ProductManager.update_product(product_id, qty, price, per, unit)
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
        try:
            product_id = int(request.POST.get("product_id"))
            quantity = int(request.POST.get("quantity"))

            email = request.session.get("email")
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if not row:
                return JsonResponse({"success": False, "message": "User not found"})

            buyer_id = row[0]
            success, msg = ProductManager.purchase_product(product_id, quantity, buyer_id)
            return JsonResponse({"success": success, "message": msg})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Server error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Unauthorized or bad request"})

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
            "category": p[6] if len(p) > 6 else "uncategorized"
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
    
def get_negotiation_dashboard(request):
    if 'user_id' not in request.session or 'role' not in request.session:
        return JsonResponse({"error": "Not logged in"}, status=403)

    user_id = request.session['user_id']
    role = request.session['role']

    data = get_negotiation_dashboard_data(user_id, role)
    return JsonResponse({"records": data})
    
@csrf_exempt
def save_bargain_setting(request):
    if request.method == "POST":
        product_id = int(request.POST.get("product_id"))
        min_quantity = int(request.POST.get("min_quantity"))
        min_price = float(request.POST.get("min_price"))

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT unit FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            return JsonResponse({"success": False, "error": "Product not found"})
        unit = row[0]

        setting = BargainFactory.create_setting(product_id, min_quantity, min_price)
        setting.save()

        return JsonResponse({"success": True, "unit": unit})

    return JsonResponse({"success": False, "error": "Invalid request"})

@csrf_exempt
def save_bargain_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = request.session.get("user_id", 1)
        req = BargainFactory.create_request(
            data["product_id"], user_id, data["quantity"], data["price"]
        )
        req.save()
        return JsonResponse({"status": "success"})

@csrf_exempt
def get_bargain_setting_with_unit(request, bargain_setting_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bs.id, bs.product_id, bs.min_quantity, bs.min_price, p.unit
        FROM bargain_settings bs
        JOIN products p ON bs.product_id = p.id
        WHERE bs.id = ?
    """, (bargain_setting_id,))
    row = cursor.fetchone()
    if row:
        return JsonResponse({
            "id": row[0],
            "product_id": row[1],
            "min_quantity": row[2],
            "min_price": row[3],
            "unit": row[4]
        })
    return JsonResponse({"error": "Not found"}, status=404)

def get_negotiation_tasks_view(request):
    if 'email' not in request.session or 'role' not in request.session:
        return JsonResponse({"tasks": []})

    email = request.session['email']
    role = request.session['role']
    tasks = get_negotiation_tasks(email, role)
    return JsonResponse({"tasks": tasks})


def get_orders(request):
    if 'email' not in request.session or 'role' not in request.session:
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=403)

    email = request.session['email']
    role = request.session['role']

    orders = get_orders_for_user(email, role)
    return JsonResponse({"orders": orders})


@csrf_exempt
def submit_negotiation_response(request):
    if request.method == "POST":
        data = json.loads(request.body)

        bargain_id = data.get("bargain_id")
        quantity = data.get("quantity")
        price = data.get("price")
        comment = data.get("comment")
        status = data.get("status")

        # Get seller_id from session
        seller_id = request.session.get("user_id")
        if not request.session.get("user_id"):
            return JsonResponse({"error": "User not logged in"}, status=403)


        # Call backend function with correct IDs
        success, message = save_negotiation_response(
            bargain_id, quantity, price, comment, status
        )

        if success:
            return JsonResponse({"message": message})
        else:
            return JsonResponse({"error": message}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
def update_negotiation_dashboard(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            row_id = data.get("negotiation_id")  # this should be record.id from your table
            quantity = data.get("quantity")
            price = data.get("price")
            comment = data.get("comment")
            action = data.get("status")

            success, message = update_negotiation_dashboard_response(
                row_id, quantity, price, comment, action
            )

            if success:
                return JsonResponse({"message": message})
            else:
                return JsonResponse({"error": message}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
