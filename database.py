
import sqlite3


DATABASE = "rewear.db"


def add_column_if_missing(cursor, table_name, column_name, column_definition):

    columns = cursor.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if column_name not in column_names:

        cursor.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )


def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()


    # =========================================================
    # USERS TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)


    # =========================================================
    # PRODUCTS TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            price REAL NOT NULL,

            category TEXT NOT NULL,

            subcategory TEXT,

            description TEXT,

            source TEXT,

            original_price REAL,

            size TEXT,

            times_worn INTEGER,

            listing_type TEXT,

            rental_price REAL,

            rental_duration TEXT,

            security_deposit REAL,

            occasions TEXT,

            available_from TEXT,

            available_to TEXT,

            seller_id INTEGER,

            outfit_type TEXT,

            fabric TEXT,

            pattern TEXT,

            sleeve TEXT,

            image1 TEXT,

            image2 TEXT,

            image3 TEXT,

            image4 TEXT
        )
    """)


    # =========================================================
    # ADD NEW PRODUCT COLUMNS TO EXISTING DATABASE
    # =========================================================

    add_column_if_missing(
        cursor, "products", "subcategory", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "description", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "source", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "original_price", "REAL"
    )

    add_column_if_missing(
        cursor, "products", "size", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "times_worn", "INTEGER"
    )

    add_column_if_missing(
        cursor, "products", "listing_type", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "rental_price", "REAL"
    )

    add_column_if_missing(
        cursor, "products", "rental_duration", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "security_deposit", "REAL"
    )

    add_column_if_missing(
        cursor, "products", "occasions", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "available_from", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "available_to", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "seller_id", "INTEGER"
    )

    add_column_if_missing(
        cursor, "products", "outfit_type", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "fabric", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "pattern", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "sleeve", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "image1", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "image2", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "image3", "TEXT"
    )

    add_column_if_missing(
        cursor, "products", "image4", "TEXT"
    )


    # =========================================================
    # DEFAULT PRODUCTS
    # =========================================================

    existing_products = cursor.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]


    if existing_products == 0:

        products = [

            (
                "Classic White Shirt",
                299,
                "Shirts",
                "Formal"
            ),

            (
                "Blue Denim Jeans",
                499,
                "Jeans",
                "Straight Fit"
            ),

            (
                "Casual Handbag",
                399,
                "Accessories",
                "Handbags"
            ),

            (
                "Floral Summer Dress",
                599,
                "Dresses",
                "Floral"
            ),

            (
                "Casual Sneakers",
                699,
                "Footwear",
                "Sneakers"
            ),

            (
                "Denim Jacket",
                799,
                "Outerwear",
                "Denim Jackets"
            )
        ]


        cursor.executemany("""
            INSERT INTO products
            (name, price, category, subcategory)
            VALUES (?, ?, ?, ?)
        """, products)


    # =========================================================
    # CART TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_id INTEGER NOT NULL,

            quantity INTEGER NOT NULL DEFAULT 1,

            user_id INTEGER
        )
    """)


    # =========================================================
    # ORDERS TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            customer_name TEXT NOT NULL,

            phone TEXT NOT NULL,

            address TEXT NOT NULL,

            city TEXT NOT NULL,

            pin_code TEXT NOT NULL,

            payment_method TEXT NOT NULL,

            total REAL NOT NULL
        )
    """)


    # =========================================================
    # ADD user_id TO OLD ORDERS TABLE IF NEEDED
    # =========================================================

    order_columns = cursor.execute(
        "PRAGMA table_info(orders)"
    ).fetchall()


    order_column_names = [
        column[1] for column in order_columns
    ]


    if "user_id" not in order_column_names:

        cursor.execute("""
            ALTER TABLE orders
            ADD COLUMN user_id INTEGER
        """)


    # =========================================================
    # ORDER ITEMS TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            order_id INTEGER NOT NULL,

            product_id INTEGER NOT NULL,

            quantity INTEGER NOT NULL,

            price REAL NOT NULL
        )
    """)


    # =========================================================
    # RENTAL BOOKINGS TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rental_bookings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            product_id INTEGER NOT NULL,

            user_id INTEGER NOT NULL,

            start_date TEXT NOT NULL,

            end_date TEXT NOT NULL,

            rental_price REAL NOT NULL,

            security_deposit REAL NOT NULL,

            status TEXT DEFAULT 'Booked'
        )
    """)


    # =========================================================
    # WISHLIST TABLE
    # =========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            product_id INTEGER NOT NULL
        )
    """)


    # =========================================================
    # SAVE EVERYTHING
    # =========================================================

    connection.commit()

    connection.close()


    print("ReWear database updated successfully! ♻️")


if __name__ == "__main__":

    create_database()
