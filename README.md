# 🛒 Smart Bargain - v1.0.0

Smart Bargain is a web-based marketplace platform that enables buyers and sellers to negotiate product prices, track orders, and manage inventory in real time.

---

##  Live Demo

👉 [Click here to visit the deployed site](https://lakmali.pythonanywhere.com/)

---

##  Features Overview

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
| Deployment   | PythonAnywhere            |


---
🛠️ Troubleshooting Tips

🗃️ Database Not Working or Site Not Loading
Please make sure the website has been properly launched by the admin. If the site doesn’t load, try refreshing or come back later.

🔐 Login or Registration Problems
Double-check your email and password.
Make sure you’ve selected the correct user type: Buyer or Seller.
If registration fails, ensure all fields are filled correctly.

🛒 Product or Negotiation Details Not Visible
Try refreshing the page.
Make sure you are logged in.
If problems continue, contact support.

⚠️ Unauthorized Access Message
Some features are only available to certain users (e.g., only Sellers can add products).
Log out and log back in with the correct user type.

📅 Booking or Price Entry Errors
Ensure quantity and price are valid numbers.
All fields must be filled in before submitting.

📬 Contact Messages Not Working
Make sure you enter a valid email and a clear message.
After submitting, your message will be visible to sellers.
