from flask import Flask, render_template, redirect, request, session
import sqlite3
import os
from werkzeug.utils import secure_filename


DATABASE = "rewear.db"


app = Flask(__name__)

app.secret_key = "rewear_secret_key_2026"


# =========================================================
# PHOTO UPLOAD SETTINGS
# =========================================================

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# MAKE SURE PRODUCT COLUMNS EXIST
# =========================================================

def prepare_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    columns = cursor.execute(
        "PRAGMA table_info(products)"
    ).fetchall()

    existing_columns = [
        column[1]
        for column in columns
    ]

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

        "sleeve": "TEXT"
    }


    for column_name, column_type in new_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE products
                ADD COLUMN {column_name} {column_type}
                """
            )


    connection.commit()

    connection.close()


prepare_database()


# =========================================================
# GET PRODUCTS
# =========================================================

def get_products():

    connection = get_connection()

    products = connection.execute(
        """
        SELECT *
        FROM products
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return products


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

    return render_template(
        "shop.html",
        products=products
    )


# =========================================================
# PRODUCT DETAILS
# =========================================================

@app.route("/product/<int:product_id>")
def product_details(product_id):

    connection = get_connection()

    product = connection.execute(
        """
        SELECT *
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    ).fetchone()

    connection.close()


    if product is None:

        return "Product not found", 404


    return render_template(
        "product.html",
        product=product
    )


# =========================================================
# CART
# =========================================================

@app.route("/cart")
def cart():

    if "user_id" not in session:

        return redirect("/login")


    user_id = session["user_id"]


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

        JOIN products
        ON cart.product_id = products.id

        WHERE cart.user_id = ?

        ORDER BY cart.id DESC
        """,
        (user_id,)
    ).fetchall()


    total = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )


    connection.close()


    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


# =========================================================
# ADD TO CART
# =========================================================

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):

    if "user_id" not in session:

        return redirect("/login")


    user_id = session["user_id"]


    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    existing_item = cursor.execute(
        """
        SELECT id, quantity
        FROM cart
        WHERE product_id = ?
        AND user_id = ?
        """,
        (
            product_id,
            user_id
        )
    ).fetchone()


    if existing_item:

        cursor.execute(
            """
            UPDATE cart
            SET quantity = quantity + 1
            WHERE id = ?
            """,
            (existing_item[0],)
        )

    else:

        cursor.execute(
            """
            INSERT INTO cart
            (
                product_id,
                quantity,
                user_id
            )
            VALUES (?, 1, ?)
            """,
            (
                product_id,
                user_id
            )
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


    user_id = session["user_id"]


    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM cart
        WHERE id = ?
        AND user_id = ?
        """,
        (
            cart_id,
            user_id
        )
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

        # ---------------------------------------------
        # BASIC INFORMATION
        # ---------------------------------------------

        name = request.form.get(
            "name",
            ""
        ).strip()


        category = request.form.get(
            "category",
            ""
        )


        outfit_type = request.form.get(
            "outfit_type",
            ""
        )


        fabric = request.form.get(
            "fabric",
            ""
        )


        pattern = request.form.get(
            "pattern",
            ""
        )


        size = request.form.get(
            "size",
            ""
        )


        sleeve = request.form.get(
            "sleeve",
            ""
        )


        occasion = request.form.get(
            "occasion",
            ""
        )


        # ---------------------------------------------
        # STORY
        # ---------------------------------------------

        description = request.form.get(
            "description",
            ""
        ).strip()


        source = request.form.get(
            "source",
            ""
        ).strip()


        times_worn = request.form.get(
            "times_worn",
            ""
        )


        # ---------------------------------------------
        # PRICING
        # ---------------------------------------------

        original_price = request.form.get(
            "original_price",
            ""
        )


        price = request.form.get(
            "price",
            "0"
        )


        # ---------------------------------------------
        # LISTING TYPE
        # ---------------------------------------------

        listing_type = request.form.get(
            "listing_type",
            "Sell"
        )


        # ---------------------------------------------
        # RENTAL INFORMATION
        # ---------------------------------------------

        rental_price = request.form.get(
            "rental_price",
            ""
        )


        rental_duration = request.form.get(
            "rental_duration",
            ""
        )


        security_deposit = request.form.get(
            "security_deposit",
            ""
        )


        available_from = request.form.get(
            "available_from",
            ""
        )


        available_to = request.form.get(
            "available_to",
            ""
        )


        # ---------------------------------------------
        # CONVERT EMPTY NUMBERS TO NULL
        # ---------------------------------------------

        def number_or_none(value):

            if value == "":

                return None

            return value


        original_price = number_or_none(
            original_price
        )


        times_worn = number_or_none(
            times_worn
        )


        rental_price = number_or_none(
            rental_price
        )


        security_deposit = number_or_none(
            security_deposit
        )


        # ---------------------------------------------
        # UPLOAD PHOTOS
        # ---------------------------------------------

        uploaded_images = request.files.getlist(
            "images"
        )


        image_names = []


        for image in uploaded_images:

            if image and image.filename:

                if allowed_file(image.filename):

                    original_filename = secure_filename(
                        image.filename
                    )


                    filename = (
                        str(session["user_id"])
                        + "_"
                        + str(os.getpid())
                        + "_"
                        + str(len(image_names) + 1)
                        + "_"
                        + original_filename
                    )


                    image_path = os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )


                    image.save(image_path)


                    image_names.append(
                        filename
                    )


                if len(image_names) == 4:

                    break


        while len(image_names) < 4:

            image_names.append(None)


        image1 = image_names[0]

        image2 = image_names[1]

        image3 = image_names[2]

        image4 = image_names[3]


        # ---------------------------------------------
        # SAVE PRODUCT
        # ---------------------------------------------

        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()


        cursor.execute(
            """
            INSERT INTO products

            (
                name,
                price,
                category,

                description,
                source,
                original_price,
                size,
                times_worn,

                listing_type,
                rental_price,
                rental_duration,
                security_deposit,

                occasions,
                available_from,
                available_to,

                seller_id,

                image1,
                image2,
                image3,
                image4,

                outfit_type,
                fabric,
                pattern,
                sleeve
            )

            VALUES
            (
                ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?,
                ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?
            )
            """,

            (
                name,

                price,

                category,

                description,

                source,

                original_price,

                size,

                times_worn,

                listing_type,

                rental_price,

                rental_duration,

                security_deposit,

                occasion,

                available_from,

                available_to,

                session["user_id"],

                image1,

                image2,

                image3,

                image4,

                outfit_type,

                fabric,

                pattern,

                sleeve
            )
        )


        connection.commit()

        connection.close()


        return redirect("/shop")


    return render_template(
        "sell.html"
    )


# =========================================================
# CHECKOUT
# =========================================================

@app.route("/checkout")
def checkout():

    if "user_id" not in session:

        return redirect("/login")


    user_id = session["user_id"]


    connection = get_connection()


    cart_items = connection.execute(
        """
        SELECT
            products.name,
            products.price,
            cart.quantity

        FROM cart

        JOIN products
        ON cart.product_id = products.id

        WHERE cart.user_id = ?
        """,
        (user_id,)
    ).fetchall()


    total = sum(
        item["price"] * item["quantity"]
        for item in cart_items
    )


    connection.close()


    return render_template(
        "checkout.html",
        cart_items=cart_items,
        total=total
    )


# =========================================================
# PLACE ORDER
# =========================================================

@app.route("/place_order", methods=["POST"])
def place_order():

    if "user_id" not in session:

        return redirect("/login")


    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()


    customer_name = request.form[
        "customer_name"
    ]

    phone = request.form[
        "phone"
    ]

    address = request.form[
        "address"
    ]

    city = request.form[
        "city"
    ]

    pin_code = request.form[
        "pin_code"
    ]

    payment_method = request.form[
        "payment_method"
    ]


    user_id = session["user_id"]


    # Get this user's cart

    cart_items = cursor.execute(
        """
        SELECT
            products.id,
            products.price,
            cart.quantity

        FROM cart

        JOIN products
        ON cart.product_id = products.id

        WHERE cart.user_id = ?
        """,
        (user_id,)
    ).fetchall()


    total = sum(
        price * quantity
        for product_id, price, quantity
        in cart_items
    )


    # Save order

    cursor.execute(
        """
        INSERT INTO orders

        (
            user_id,
            customer_name,
            phone,
            address,
            city,
            pin_code,
            payment_method,
            total
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            user_id,
            customer_name,
            phone,
            address,
            city,
            pin_code,
            payment_method,
            total
        )
    )


    order_id = cursor.lastrowid


    # Save order items

    for product_id, price, quantity in cart_items:

        cursor.execute(
            """
            INSERT INTO order_items

            (
                order_id,
                product_id,
                quantity,
                price
            )

            VALUES (?, ?, ?, ?)
            """,

            (
                order_id,
                product_id,
                quantity,
                price
            )
        )


    # Clear user's cart

    cursor.execute(
        """
        DELETE FROM cart
        WHERE user_id = ?
        """,
        (user_id,)
    )


    connection.commit()

    connection.close()


    return redirect("/orders")


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form[
            "name"
        ]

        email = request.form[
            "email"
        ]

        password = request.form[
            "password"
        ]


        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()


        try:

            cursor.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password
                )

                VALUES (?, ?, ?)
                """,

                (
                    name,
                    email,
                    password
                )
            )


            connection.commit()


        except sqlite3.IntegrityError:

            connection.close()


            return """
            <h2>Email already registered!</h2>

            <a href="/register">
                Try another email
            </a>
            """


        connection.close()


        return redirect("/login")


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form[
            "email"
        ]

        password = request.form[
            "password"
        ]


        connection = get_connection()


        user = connection.execute(
            """
            SELECT *
            FROM users

            WHERE email = ?
            AND password = ?
            """,

            (
                email,
                password
            )
        ).fetchone()


        connection.close()


        if user:

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]

            session["user_email"] = user["email"]


            return redirect("/")


        else:

            return """
            <h1>Login Failed ❌</h1>

            <p>
                Incorrect email or password.
            </p>

            <a href="/login">
                Try Again
            </a>
            """


    return render_template(
        "login.html"
    )


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
        SELECT *
        FROM orders

        WHERE user_id = ?

        ORDER BY id DESC
        """,

        (
            session["user_id"],
        )
    ).fetchall()


    orders = []


    for order in orders_data:

        items_data = connection.execute(
            """
            SELECT
                order_items.quantity,
                order_items.price,
                products.name

            FROM order_items

            JOIN products
            ON order_items.product_id = products.id

            WHERE order_items.order_id = ?
            """,

            (
                order["id"],
            )
        ).fetchall()


        order_data = dict(order)


        order_data[
            "order_products"
        ] = items_data


        orders.append(
            order_data
        )


    connection.close()


    return render_template(
        "orders.html",
        orders=orders
    )


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

    app.run(
        debug=True
    )