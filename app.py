import os
import sqlite3
from flask import Flask, render_template, redirect, request, session
from werkzeug.utils import secure_filename
from database import create_database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "rewear.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "rewear-local-dev-key")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

create_database()


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def prepare_database():
    connection = get_connection()

    new_columns = {
        "description": "TEXT",
        "source": "TEXT",
        "original_price": "REAL",
        "size": "TEXT",
        "times_worn": "INTEGER",
        "listing_type": "TEXT",
        "rental_price": "REAL",
        "rental_duration": "TEXT",
        "security_deposit": "REAL",
        "occasions": "TEXT",
        "available_from": "TEXT",
        "available_to": "TEXT",
        "seller_id": "INTEGER",
        "image1": "TEXT",
        "image2": "TEXT",
        "image3": "TEXT",
        "image4": "TEXT",
        "outfit_type": "TEXT",
        "fabric": "TEXT",
        "pattern": "TEXT",
        "sleeve": "TEXT",
    }

    existing_columns = {
        row["name"]
        for row in connection.execute(
            "PRAGMA table_info(products)"
        ).fetchall()
    }

    for column_name, column_type in new_columns.items():
        if column_name not in existing_columns:
            connection.execute(
                f"ALTER TABLE products ADD COLUMN {column_name} {column_type}"
            )

    connection.commit()
    connection.close()


prepare_database()


# =========================================================
# HELPERS
# =========================================================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def get_products():
    connection = get_connection()
    products = connection.execute(
        "SELECT * FROM products ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return products


def number_or_none(value):
    value = (value or "").strip()
    return value if value else None


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# SHOP
# =========================================================

@app.route("/shop")
def shop():
    products = get_products()
    return render_template("shop.html", products=products)


# =========================================================
# PRODUCT DETAILS
# =========================================================

@app.route("/product/<int:product_id>")
def product_details(product_id):
    connection = get_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    connection.close()

    if product is None:
        return "Product not found", 404

    return render_template("product.html", product=product)


# =========================================================
# CART
# =========================================================

@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()

    cart_items = connection.execute(
        """
        SELECT
            cart.id AS cart_id,
            products.name,
            products.price,
            products.image1,
            cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = ?
        ORDER BY cart.id DESC
        """,
        (session["user_id"],),
    ).fetchall()

    total = sum(
        (item["price"] or 0) * item["quantity"]
        for item in cart_items
    )

    connection.close()

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total,
    )


# =========================================================
# ADD TO CART
# =========================================================

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    connection = get_connection()

    product = connection.execute(
        "SELECT id FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if product is None:
        connection.close()
        return "Product not found", 404

    existing_item = connection.execute(
        """
        SELECT id, quantity FROM cart
        WHERE product_id = ? AND user_id = ?
        """,
        (product_id, user_id),
    ).fetchone()

    if existing_item:
        connection.execute(
            "UPDATE cart SET quantity = quantity + 1 WHERE id = ?",
            (existing_item["id"],),
        )
    else:
        connection.execute(
            """
            INSERT INTO cart (product_id, quantity, user_id)
            VALUES (?, 1, ?)
            """,
            (product_id, user_id),
        )

    connection.commit()
    connection.close()

    return redirect("/cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

@app.route("/remove_from_cart/<int:cart_id>")
def remove_from_cart(cart_id):
    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()

    connection.execute(
        "DELETE FROM cart WHERE id = ? AND user_id = ?",
        (cart_id, session["user_id"]),
    )

    connection.commit()
    connection.close()

    return redirect("/cart")


# =========================================================
# SELL / LIST OUTFIT
# =========================================================

@app.route("/sell", methods=["GET", "POST"])
def sell():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        outfit_type = request.form.get("outfit_type", "").strip()
        fabric = request.form.get("fabric", "").strip()
        pattern = request.form.get("pattern", "").strip()
        size = request.form.get("size", "").strip()
        sleeve = request.form.get("sleeve", "").strip()
        occasion = request.form.get("occasion", "").strip()

        description = request.form.get("description", "").strip()
        source = request.form.get("source", "").strip()
        times_worn = number_or_none(request.form.get("times_worn"))

        original_price = number_or_none(
            request.form.get("original_price")
        )
        price = number_or_none(request.form.get("price")) or "0"

        listing_type = request.form.get("listing_type", "Sell").strip()
        rental_price = number_or_none(request.form.get("rental_price"))
        rental_duration = request.form.get("rental_duration", "").strip()
        security_deposit = number_or_none(
            request.form.get("security_deposit")
        )
        available_from = request.form.get("available_from", "").strip()
        available_to = request.form.get("available_to", "").strip()

        uploaded_images = request.files.getlist("images")
        image_names = []

        for image in uploaded_images:
            if not image or not image.filename:
                continue

            if not allowed_file(image.filename):
                continue

            original_filename = secure_filename(image.filename)
            filename = (
                f"{session['user_id']}_{os.urandom(8).hex()}_"
                f"{original_filename}"
            )

            image.save(
                os.path.join(app.config["UPLOAD_FOLDER"], filename)
            )
            image_names.append(filename)

            if len(image_names) == 4:
                break

        while len(image_names) < 4:
            image_names.append(None)

        connection = get_connection()

        connection.execute(
            """
            INSERT INTO products (
                name, price, category, description, source,
                original_price, size, times_worn, listing_type,
                rental_price, rental_duration, security_deposit,
                occasions, available_from, available_to, seller_id,
                image1, image2, image3, image4,
                outfit_type, fabric, pattern, sleeve
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                name, price, category, description, source,
                original_price, size, times_worn, listing_type,
                rental_price, rental_duration, security_deposit,
                occasion, available_from, available_to,
                session["user_id"],
                image_names[0], image_names[1],
                image_names[2], image_names[3],
                outfit_type, fabric, pattern, sleeve,
            ),
        )

        connection.commit()
        connection.close()

        return redirect("/shop")

    return render_template("sell.html")


# =========================================================
# CHECKOUT
# =========================================================

@app.route("/checkout")
def checkout():
    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()

    cart_items = connection.execute(
        """
        SELECT products.name, products.price, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.user_id = ?
        """,
        (session["user_id"],),
    ).fetchall()

    total = sum(
        (item["price"] or 0) * item["quantity"]
        for item in cart_items
    )

    connection.close()

    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total,
    )


# =========================================================
# PLACE ORDER
# =========================================================

@app.route("/place_order", methods=["POST"])
def place_order():
    if "user_id" not in session:
        return redirect("/login")

    customer_name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    city = request.form.get("city", "").strip()
    pin_code = request.form.get("pin_code", "").strip()
    payment_method = request.form.get("payment_method", "").strip()

    user_id = session["user_id"]
    connection = get_connection()

    try:
        cart_items = connection.execute(
            """
            SELECT products.id, products.price, cart.quantity
            FROM cart
            JOIN products ON cart.product_id = products.id
            WHERE cart.user_id = ?
            """,
            (user_id,),
        ).fetchall()

        if not cart_items:
            connection.close()
            return redirect("/cart")

        total = sum(
            (item["price"] or 0) * item["quantity"]
            for item in cart_items
        )

        cursor = connection.execute(
            """
            INSERT INTO orders (
                user_id, customer_name, phone, address,
                city, pin_code, payment_method, total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, customer_name, phone, address,
                city, pin_code, payment_method, total,
            ),
        )

        order_id = cursor.lastrowid

        for item in cart_items:
            connection.execute(
                """
                INSERT INTO order_items (
                    order_id, product_id, quantity, price
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    order_id,
                    item["id"],
                    item["quantity"],
                    item["price"],
                ),
            )

        connection.execute(
            "DELETE FROM cart WHERE user_id = ?",
            (user_id,),
        )

        connection.commit()

    except sqlite3.Error:
        connection.rollback()
        connection.close()
        raise

    connection.close()

    return redirect("/orders")


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
                """,
                (name, email, password),
            )
            connection.commit()

        except sqlite3.IntegrityError:
            connection.close()
            return """
                <h2>Email already registered!</h2>
                <a href="/register">Try another email</a>
            """

        connection.close()
        return redirect("/login")

    return render_template("register.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        connection = get_connection()

        user = connection.execute(
            """
            SELECT * FROM users
            WHERE email = ? AND password = ?
            """,
            (email, password),
        ).fetchone()

        connection.close()

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            return redirect("/")

        return """
            <h1>Login Failed ❌</h1>
            <p>Incorrect email or password.</p>
            <a href="/login">Try Again</a>
        """

    return render_template("login.html")


# =========================================================
# MY ORDERS
# =========================================================

@app.route("/orders")
def orders():
    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()

    orders_data = connection.execute(
        """
        SELECT * FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],),
    ).fetchall()

    orders_list = []

    for order in orders_data:
        items_data = connection.execute(
            """
            SELECT
                order_items.quantity,
                order_items.price,
                products.name
            FROM order_items
            JOIN products ON order_items.product_id = products.id
            WHERE order_items.order_id = ?
            """,
            (order["id"],),
        ).fetchall()

        order_data = dict(order)
        order_data["order_products"] = items_data
        orders_list.append(order_data)

    connection.close()

    return render_template("orders.html", orders=orders_list)


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)