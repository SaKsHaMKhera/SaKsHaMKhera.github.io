from flask import Flask, render_template, request

app = Flask(__name__)

# Menu Items
menu = {
    "Burger": 120,
    "Pizza": 250,
    "Pasta": 180,
    "Coffee": 80,
    "Ice Cream": 100
}

# ================================
# HOME PAGE (WITH PREVIOUS ORDERS)
# ================================
@app.route('/')
def home():

    # Load previous orders
    try:
        with open("orders.txt", "r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        data = ""

    return render_template('index.html', menu=menu, data=data)


# ================================
# BILL PAGE
# ================================
@app.route('/bill', methods=['POST'])
def bill():
    customer_name = request.form.get("customer_name")
    phone = request.form.get("phone")

    order = {}
    total = 0

    for item, price in menu.items():
        qty = int(request.form.get(item, 0))
        if qty > 0:
            subtotal = qty * price
            total += subtotal
            order[item] = {"qty": qty, "subtotal": subtotal}

    gst = round(total * 0.05, 2)
    final_total = round(total + gst, 2)

    # Save order as unpaid
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(f"\n📝 New Order (UNPAID) - {customer_name} ({phone})\n")
        for item, details in order.items():
            f.write(f"{item} × {details['qty']} = ₹{details['subtotal']}\n")
        f.write(f"GST: ₹{gst}\n")
        f.write(f"Total: ₹{final_total}\n")
        f.write("-" * 40 + "\n")

    return render_template(
        'bill.html',
        order=order,
        gst=gst,
        final=final_total,
        customer_name=customer_name,
        phone=phone
    )


# ================================
# PAYMENT PAGE
# ================================
@app.route('/pay', methods=['POST'])
def pay():
    customer_name = request.form.get("customer_name")
    phone = request.form.get("phone")
    final = request.form.get("final")

    return render_template(
        'payment.html',
        customer_name=customer_name,
        phone=phone,
        final=final
    )


# ================================
# PAYMENT SUCCESS PAGE
# ================================
@app.route('/payment_success', methods=['POST'])
def payment_success():
    customer_name = request.form.get("customer_name")
    phone = request.form.get("phone")
    method = request.form.get("method")
    amount = request.form.get("amount")  # keep as string (no int conversion)

    # Save paid order info
    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(f"💰 PAYMENT SUCCESS - {customer_name} ({phone})\n")
        f.write(f"Amount Paid: ₹{amount}\n")
        f.write(f"Mode: {method}\n")
        f.write("=" * 40 + "\n")

    return render_template(
        'success.html',
        customer_name=customer_name,
        phone=phone,
        method=method,
        amount=amount
    )


# ================================
# OPTIONAL: SEPARATE PREVIOUS ORDERS PAGE
# ================================
@app.route('/previous_orders')
def previous_orders():

    try:
        with open("orders.txt", "r", encoding="utf-8") as f:
            data = f.read()
    except:
        data = "No orders yet."

    return render_template("previous_orders.html", data=data)



if __name__ == '__main__':
    app.run(debug=True)
