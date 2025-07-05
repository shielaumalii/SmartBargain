from django.http import JsonResponse
from .database import create_connection
from .bargain_factory import BargainFactory

def get_negotiation_tasks(email, role):
    conn = create_connection()
    cursor = conn.cursor()

    if role == 'buyer':
        # Match email with bargain_requests.buyer_id via users
        cursor.execute("""
            SELECT br.id, p.name AS product, br.quantity, br.status, br.price
            FROM bargain_requests br
            JOIN products p ON br.product_id = p.id
            JOIN users u ON br.user_id = u.id
            WHERE u.email = ?
            ORDER BY br.created_at DESC
        """, (email,))
    
    elif role == 'seller':
        # Match email with products.seller_id via users
        cursor.execute("""
            SELECT br.id, p.name AS product, br.quantity, br.status, br.price
            FROM bargain_requests br
            JOIN products p ON br.product_id = p.id
            JOIN users u ON p.seller_id = u.id
            WHERE u.email = ?
            ORDER BY br.created_at DESC
        """, (email,))
    
    else:
        return []

    rows = cursor.fetchall()
    tasks = []
    for row in rows:
        task = {
            "id": row[0],
            "product": row[1],
            "quantity": row[2],
            "status": row[3],
            "price": row[4],
        }
        tasks.append(task)

    return tasks

def update_negotiation_status_in_db(task_id, new_status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE bargain_requests SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()

def save_negotiation_response(bargain_id, quantity, price, comment, action, conn=None):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Map action to status
        status_map = {
            "accept": "Active",
            "reject": "Rejected",
            "counter": "Pending Buyer Approval",
            "cancel": "Cancelled"
        }

        status = status_map.get(action.lower())
        if not status:
            return False, "Invalid action"

        # Get buyer_id and product_id from bargain_requests
        cursor.execute("SELECT user_id, product_id FROM bargain_requests WHERE id = ?", (bargain_id,))
        result = cursor.fetchone()
        if not result:
            return False, "Invalid bargain ID"
        buyer_id, product_id = result

        # Get seller_id from products table
        cursor.execute("SELECT seller_id FROM products WHERE id = ?", (product_id,))
        seller_result = cursor.fetchone()
        if not seller_result:
            return False, "Seller not found"
        seller_id = seller_result[0]

        # Update bargain_requests status
        cursor.execute("UPDATE bargain_requests SET status = ? WHERE id = ?", (status, bargain_id))

        # ✅ Insert including product_id
        cursor.execute("""
            INSERT INTO negotiation_dashboard (
                bargain_id, product_id, proposed_quantity, proposed_price, comment,
                status, buyer_id, seller_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (bargain_id, product_id, quantity, price, comment, status, buyer_id, seller_id))

        # Delete from bargain_requests
        cursor.execute("DELETE FROM bargain_requests WHERE id = ?", (bargain_id,))

        conn.commit()
        return True, "Response saved successfully"

    except Exception as e:
        return False, str(e)

#This was to focus on getting orders based on buyer id       
def get_orders_for_user_id(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.id, p.name, o.quantity, o.price, o.created_at
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.buyer_id = ?
    """, (user_id,))


    rows = cursor.fetchall()
    orders = []

    for row in rows:
        orders.append({
            "id": row[0],
            "product": row[1],
            "qty": row[2],
            "price": row[3],
            "date": row[4],
            "status": "Purchased"
        })

    return orders

# This is to get orders for sellers 
def get_orders_for_seller(seller_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.id, p.name, o.quantity, o.price, o.created_at, u.email
        FROM orders o
        JOIN products p ON o.product_id = p.id
        JOIN users u ON o.buyer_id = u.id
        WHERE p.seller_id = ?
        ORDER BY o.created_at DESC
    """, (seller_id,))

    rows = cursor.fetchall()
    orders = []

    for row in rows:
        orders.append({
            "id": row[0],
            "product": row[1],
            "qty": row[2],
            "price": row[3],
            "date": row[4],
            "buyer": row[5],  # include buyer email for seller context
            "status": "Purchased"
        })

    return orders


#Show orders based on buyer id or seller id
def get_orders(request):
    print("🚨 /get_orders triggered")
    user_id = request.session.get('user_id')
    role = request.session.get('role')

    if not user_id or not role:
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=403)

    if role == 'buyer':
        orders = get_orders_for_user_id(user_id)
    elif role == 'seller':
        orders = get_orders_for_seller(user_id)
    else:
        return JsonResponse({"success": False, "message": "Invalid role"}, status=400)
    print(f"📦 Orders fetched: {len(orders)}")
    return JsonResponse({"orders": orders})



def get_negotiation_dashboard_data(user_id, role, status_filter=None):
    conn = create_connection()
    cursor = conn.cursor()

    base_query = """
        SELECT nd.id, p.name, nd.proposed_quantity, nd.proposed_price,
               nd.comment, nd.status, ub.name as buyer_name, us.name as seller_name
        FROM negotiation_dashboard nd
        JOIN products p ON nd.product_id = p.id
        JOIN users ub ON nd.buyer_id = ub.id
        JOIN users us ON nd.seller_id = us.id
    """

    if role == 'buyer':
        cursor.execute(base_query + " WHERE nd.buyer_id = ? ORDER BY nd.id DESC", (user_id,))
    elif role == 'seller':
        cursor.execute(base_query + " WHERE nd.seller_id = ? ORDER BY nd.id DESC", (user_id,))
    else:
        return []

    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "product": row[1],
            "quantity": row[2],
            "price": row[3],
            "comment": row[4],
            "status": row[5],
            "buyer": row[6],
            "seller": row[7],
        })

    return result
    
    #This is to add values from seocnd negotiation groid to its table. Overwrite the values
def update_negotiation_dashboard_response(row_id, quantity, price, comment, action, status=None):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # ✅ NEW normalization logic
        normalized_map = {
            "accept": "Accepted",
            "reject": "Rejected",
            "cancel": "Cancelled",
        }

        # Normalize status even if it's provided
        base_status = status or action
        final_status = normalized_map.get(base_status.lower(), base_status)

        cursor.execute("""
            UPDATE negotiation_dashboard
            SET proposed_quantity = ?, proposed_price = ?, comment = ?, status = ?
            WHERE id = ?
        """, (quantity, price, comment, final_status, row_id))

        conn.commit()
        return True, "Negotiation updated successfully"
    except Exception as e:
        return False, str(e)


