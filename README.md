# 🛒 Smart Bargain

Smart Bargain is a web-based marketplace platform that enables buyers and sellers to negotiate product prices, track orders, and manage inventory in real time.

---

##  Live Demo

👉 [Click here to visit the deployed site](https://lakmali.pythonanywhere.com/)

---

##  Features

###  User Roles
- **Buyer**: Browse products, initiate bargain requests, purchase items.
- **Seller**: Add/edit/delete products, set bargain rules, respond to negotiations.

###  Product & Bargain Management
- Sellers set minimum quantity and price per product.
- Buyers submit bargain offers.
- Sellers can accept, reject, or counter.

###  Dashboard
- View active negotiations, order history, and messages.
- Filter and manage bargain tasks and purchase records.

###  Contact System
- Anyone (even guests) can submit contact messages.
- Sellers can view, respond, and close messages from their dashboard.

---

## 🛠 Tech Stack

| Layer        | Technology               |
|--------------|---------------------------|
| Backend      | Python, Django            |
| Frontend     | HTML, CSS, JavaScript     |
| Database     | SQLite (via Singleton DB) |
| Patterns     | Singleton, Factory        |
| Deployment   | Render / Vercel / YourHost |


---

##  Project Structure

SmartBargain/
├── core/
│ ├── backend/
│ │ ├── database.py
│ │ ├── login.py
│ │ ├── user_factory.py
│ │ ├── product_manager.py
│ │ ├── bargain_factory.py
│ │ ├── dashboard.py
│ │ └── contact_manager.py
│ ├── templates/core/
│ │ └── *.html
│ ├── static/core/
│ ├── views.py
│ └── urls.py
├── db/
│ └── smartbargain.db
├── manage.py
└── README.md
