import sqlite3

DATABASE = "rewear.db"


products = [

    # =====================================================
    # DRESSES
    # =====================================================

    ("Black Bodycon Dress", 549, "Dresses", "Bodycon Dress",
     "Elegant black bodycon dress for parties and evenings.",
     "Cotton Blend", "Solid"),

    ("Floral Maxi Dress", 699, "Dresses", "Maxi Dress",
     "Flowy floral maxi dress perfect for summer outings.",
     "Rayon", "Floral"),

    ("Pink Mini Dress", 449, "Dresses", "Mini Dress",
     "Cute pink mini dress for casual outings.",
     "Polyester", "Solid"),

    ("Lavender Midi Dress", 599, "Dresses", "Midi Dress",
     "Soft lavender midi dress with a comfortable fit.",
     "Rayon", "Solid"),

    ("White A-Line Dress", 499, "Dresses", "A-Line Dress",
     "Classic white A-line dress for casual occasions.",
     "Cotton", "Solid"),

    ("Red Wrap Dress", 649, "Dresses", "Wrap Dress",
     "Stylish red wrap dress with a flattering silhouette.",
     "Georgette", "Solid"),

    ("Satin Slip Dress", 749, "Dresses", "Slip Dress",
     "Elegant satin slip dress for evening occasions.",
     "Satin", "Solid"),

    ("Blue Shirt Dress", 599, "Dresses", "Shirt Dress",
     "Relaxed blue shirt dress for everyday wear.",
     "Cotton", "Solid"),

    ("Floral Skater Dress", 549, "Dresses", "Skater Dress",
     "Playful floral skater dress with a flared skirt.",
     "Rayon", "Floral"),

    ("Party Fit & Flare Dress", 799, "Dresses", "Fit & Flare Dress",
     "Stylish fit and flare dress for parties.",
     "Polyester", "Printed"),

    ("Pink Frock", 399, "Dresses", "Frock",
     "Cute pink frock suitable for casual occasions.",
     "Cotton", "Solid"),

    ("Black Party Dress", 699, "Dresses", "Party Dress",
     "Chic black party dress for special occasions.",
     "Polyester", "Solid"),

    ("Yellow Floral Dress", 499, "Dresses", "Floral Dress",
     "Bright floral dress with a comfortable fit.",
     "Rayon", "Floral"),

    ("Beige Co-ord Dress", 649, "Dresses", "Co-ord Dress",
     "Minimal beige co-ord dress set.",
     "Cotton Blend", "Solid"),


    # =====================================================
    # TOPS
    # =====================================================

    ("White Crop Top", 249, "Tops", "Crop Top",
     "Simple white crop top for everyday styling.",
     "Cotton", "Solid"),

    ("Black Basic Top", 229, "Tops", "Basic Top",
     "Classic black basic top for daily wear.",
     "Cotton", "Solid"),

    ("White Tank Top", 199, "Tops", "Tank Top",
     "Comfortable white tank top.",
     "Cotton", "Solid"),

    ("Red Halter Top", 299, "Tops", "Halter Top",
     "Stylish red halter top for casual outings.",
     "Polyester", "Solid"),

    ("Black Tube Top", 279, "Tops", "Tube Top",
     "Trendy black tube top.",
     "Cotton Blend", "Solid"),

    ("Blue Off-Shoulder Top", 349, "Tops", "Off-Shoulder Top",
     "Stylish blue off-shoulder top.",
     "Rayon", "Solid"),

    ("White One-Shoulder Top", 329, "Tops", "One-Shoulder Top",
     "Modern one-shoulder top.",
     "Polyester", "Solid"),

    ("Pink Peplum Top", 349, "Tops", "Peplum Top",
     "Feminine pink peplum top.",
     "Rayon", "Solid"),

    ("Black Corset Top", 399, "Tops", "Corset Top",
     "Trendy black corset-style top.",
     "Polyester", "Solid"),

    ("Floral Ruffle Top", 329, "Tops", "Ruffle Top",
     "Pretty floral ruffle top.",
     "Rayon", "Floral"),

    ("Beige Tunic Top", 379, "Tops", "Tunic",
     "Relaxed beige tunic top.",
     "Cotton", "Solid"),

    ("Oversized Graphic Top", 349, "Tops", "Oversized Top",
     "Comfortable oversized graphic top.",
     "Cotton", "Printed"),


    # =====================================================
    # SHIRTS
    # =====================================================

    ("White Formal Shirt", 299, "Shirts", "Formal Shirt",
     "Classic white formal shirt.",
     "Cotton", "Solid"),

    ("Blue Casual Shirt", 349, "Shirts", "Casual Shirt",
     "Relaxed blue casual shirt.",
     "Cotton", "Solid"),

    ("Oversized White Shirt", 399, "Shirts", "Oversized Shirt",
     "Relaxed oversized white shirt.",
     "Cotton", "Solid"),

    ("Cropped Blue Shirt", 329, "Shirts", "Cropped Shirt",
     "Trendy cropped blue shirt.",
     "Denim", "Solid"),

    ("Denim Button Shirt", 449, "Shirts", "Denim Shirt",
     "Classic denim shirt.",
     "Denim", "Solid"),

    ("Beige Linen Shirt", 499, "Shirts", "Linen Shirt",
     "Lightweight beige linen shirt.",
     "Linen", "Solid"),

    ("Red Flannel Shirt", 399, "Shirts", "Flannel Shirt",
     "Red checked flannel shirt.",
     "Cotton", "Checked"),

    ("Satin Pink Shirt", 449, "Shirts", "Satin Shirt",
     "Elegant pink satin shirt.",
     "Satin", "Solid"),

    ("Printed Summer Shirt", 379, "Shirts", "Printed Shirt",
     "Colourful printed summer shirt.",
     "Rayon", "Printed"),

    ("Blue Striped Shirt", 349, "Shirts", "Striped Shirt",
     "Classic blue striped shirt.",
     "Cotton", "Striped"),


    # =====================================================
    # JEANS
    # =====================================================

    ("Black Skinny Jeans", 499, "Jeans", "Skinny Fit",
     "Classic black skinny-fit jeans.",
     "Denim", "Solid"),

    ("Blue Slim Fit Jeans", 499, "Jeans", "Slim Fit",
     "Classic blue slim-fit jeans.",
     "Denim", "Solid"),

    ("Blue Straight Fit Jeans", 549, "Jeans", "Straight Fit",
     "Classic straight-fit blue jeans.",
     "Denim", "Solid"),

    ("Light Blue Mom Fit Jeans", 599, "Jeans", "Mom Fit",
     "Comfortable high-waisted mom fit jeans.",
     "Denim", "Solid"),

    ("Classic Boyfriend Jeans", 599, "Jeans", "Boyfriend Fit",
     "Relaxed boyfriend-fit jeans.",
     "Denim", "Solid"),

    ("Black Baggy Jeans", 649, "Jeans", "Baggy Fit",
     "Trendy relaxed baggy jeans.",
     "Denim", "Solid"),

    ("Wide-Leg Blue Jeans", 649, "Jeans", "Wide-Leg",
     "Stylish wide-leg denim jeans.",
     "Denim", "Solid"),

    ("Blue Bootcut Jeans", 599, "Jeans", "Bootcut",
     "Classic bootcut jeans.",
     "Denim", "Solid"),

    ("Dark Blue Flared Jeans", 649, "Jeans", "Flared",
     "Stylish flared jeans.",
     "Denim", "Solid"),

    ("Black Low-Rise Jeans", 549, "Jeans", "Low-Rise",
     "Trendy low-rise black jeans.",
     "Denim", "Solid"),

    ("Blue Mid-Rise Jeans", 549, "Jeans", "Mid-Rise",
     "Comfortable mid-rise jeans.",
     "Denim", "Solid"),

    ("Dark Blue High-Rise Jeans", 599, "Jeans", "High-Rise",
     "Classic high-rise jeans.",
     "Denim", "Solid"),


    # =====================================================
    # BOTTOMWEAR
    # =====================================================

    ("Black Formal Trousers", 449, "Bottomwear", "Trousers",
     "Classic black trousers.",
     "Polyester", "Solid"),

    ("Green Cargo Pants", 499, "Bottomwear", "Cargo Pants",
     "Relaxed cargo pants with utility pockets.",
     "Cotton", "Solid"),

    ("Beige Wide-Leg Pants", 499, "Bottomwear", "Wide-Leg Pants",
     "Flowy beige wide-leg pants.",
     "Rayon", "Solid"),

    ("Printed Palazzo Pants", 449, "Bottomwear", "Palazzos",
     "Comfortable printed palazzo pants.",
     "Rayon", "Printed"),

    ("Denim Shorts", 349, "Bottomwear", "Shorts",
     "Casual denim shorts.",
     "Denim", "Solid"),

    ("Black Mini Skirt", 349, "Bottomwear", "Mini Skirt",
     "Classic black mini skirt.",
     "Polyester", "Solid"),

    ("Brown Midi Skirt", 399, "Bottomwear", "Midi Skirt",
     "Elegant brown midi skirt.",
     "Rayon", "Solid"),

    ("Floral Maxi Skirt", 449, "Bottomwear", "Maxi Skirt",
     "Flowy floral maxi skirt.",
     "Rayon", "Floral"),

    ("Grey Joggers", 399, "Bottomwear", "Joggers",
     "Comfortable grey joggers.",
     "Cotton", "Solid"),

    ("Black Leggings", 299, "Bottomwear", "Leggings",
     "Stretchable black leggings.",
     "Cotton Blend", "Solid"),


    # =====================================================
    # ETHNIC WEAR
    # =====================================================

    ("Pink Cotton Kurti", 399, "Ethnic Wear", "Kurti",
     "Beautiful pink cotton kurti.",
     "Cotton", "Printed"),

    ("Blue Kurta Set", 599, "Ethnic Wear", "Kurta Set",
     "Elegant blue kurta set.",
     "Cotton", "Printed"),

    ("Floral Anarkali", 699, "Ethnic Wear", "Anarkali",
     "Flowy floral anarkali dress.",
     "Georgette", "Floral"),

    ("Maroon Salwar Suit", 749, "Ethnic Wear", "Salwar Suit",
     "Traditional maroon salwar suit.",
     "Cotton", "Printed"),

    ("Pink Sharara Set", 799, "Ethnic Wear", "Sharara Set",
     "Festive pink sharara set.",
     "Georgette", "Embroidered"),

    ("Green Lehenga", 999, "Ethnic Wear", "Lehenga",
     "Beautiful festive green lehenga.",
     "Georgette", "Embroidered"),

    ("Red Saree", 699, "Ethnic Wear", "Saree",
     "Elegant red saree.",
     "Silk Blend", "Solid"),

    ("Half Saree Set", 899, "Ethnic Wear", "Half Saree",
     "Traditional half saree set.",
     "Silk Blend", "Embroidered"),

    ("Beige Palazzo Set", 599, "Ethnic Wear", "Palazzo Set",
     "Comfortable ethnic palazzo set.",
     "Rayon", "Printed"),

    ("Pink Churidar Set", 549, "Ethnic Wear", "Churidar Set",
     "Pretty pink churidar set.",
     "Cotton", "Printed"),

    ("Blue Ethnic Dress", 649, "Ethnic Wear", "Ethnic Dress",
     "Elegant blue ethnic dress.",
     "Rayon", "Printed"),

    ("Ethnic Co-ord Set", 699, "Ethnic Wear", "Ethnic Co-ord",
     "Modern ethnic co-ord set.",
     "Cotton", "Printed"),


    # =====================================================
    # OUTERWEAR
    # =====================================================

    ("Classic Denim Jacket", 799, "Outerwear", "Denim Jacket",
     "Classic blue denim jacket.",
     "Denim", "Solid"),

    ("Black Leather Jacket", 999, "Outerwear", "Leather Jacket",
     "Classic black leather-look jacket.",
     "Faux Leather", "Solid"),

    ("Black Bomber Jacket", 899, "Outerwear", "Bomber Jacket",
     "Trendy black bomber jacket.",
     "Polyester", "Solid"),

    ("Cropped Beige Jacket", 699, "Outerwear", "Cropped Jacket",
     "Stylish cropped jacket.",
     "Cotton Blend", "Solid"),

    ("Oversized Black Jacket", 749, "Outerwear", "Oversized Jacket",
     "Relaxed oversized jacket.",
     "Polyester", "Solid"),

    ("Black Blazer", 899, "Outerwear", "Blazer",
     "Classic black blazer.",
     "Polyester", "Solid"),

    ("Beige Trench Coat", 999, "Outerwear", "Trench Coat",
     "Elegant beige trench coat.",
     "Cotton Blend", "Solid"),

    ("Brown Long Coat", 1099, "Outerwear", "Long Coat",
     "Warm brown long coat.",
     "Wool Blend", "Solid"),

    ("Lavender Cardigan", 549, "Outerwear", "Cardigan",
     "Soft lavender cardigan.",
     "Acrylic", "Solid"),

    ("Pink Shrug", 399, "Outerwear", "Shrug",
     "Lightweight pink shrug.",
     "Rayon", "Solid"),

    ("Grey Hoodie", 499, "Outerwear", "Hoodie",
     "Comfortable grey hoodie.",
     "Cotton", "Solid"),

    ("Black Sweatshirt", 449, "Outerwear", "Sweatshirt",
     "Classic black sweatshirt.",
     "Cotton", "Solid"),

    ("Cream Vest", 449, "Outerwear", "Vest",
     "Minimal cream vest.",
     "Cotton Blend", "Solid"),

    ("Printed Poncho", 499, "Outerwear", "Poncho",
     "Colourful printed poncho.",
     "Wool Blend", "Printed"),


    # =====================================================
    # ACCESSORIES
    # =====================================================

    ("Classic Black Handbag", 499, "Accessories", "Handbag",
     "Classic black handbag.",
     "Faux Leather", "Solid"),

    ("Canvas Tote Bag", 349, "Accessories", "Tote Bag",
     "Reusable canvas tote bag.",
     "Canvas", "Printed"),

    ("Brown Shoulder Bag", 449, "Accessories", "Shoulder Bag",
     "Stylish brown shoulder bag.",
     "Faux Leather", "Solid"),

    ("Beige Crossbody Bag", 399, "Accessories", "Crossbody Bag",
     "Compact beige crossbody bag.",
     "Faux Leather", "Solid"),

    ("Pearl Clutch", 499, "Accessories", "Clutch",
     "Elegant pearl-detail clutch.",
     "Synthetic", "Embellished"),

    ("Black Backpack", 549, "Accessories", "Backpack",
     "Everyday black backpack.",
     "Polyester", "Solid"),

    ("Brown Wallet", 249, "Accessories", "Wallet",
     "Compact brown wallet.",
     "Faux Leather", "Solid"),

    ("Black Leather Belt", 199, "Accessories", "Belt",
     "Classic black belt.",
     "Faux Leather", "Solid"),

    ("Brown Sunglasses", 299, "Accessories", "Sunglasses",
     "Trendy brown sunglasses.",
     "Acetate", "Solid"),

    ("Minimal Gold Watch", 699, "Accessories", "Watch",
     "Minimal gold-tone watch.",
     "Metal", "Solid"),

    ("Pearl Jewellery Set", 399, "Accessories", "Jewellery",
     "Elegant pearl jewellery set.",
     "Pearl", "Pearl"),

    ("Gold-Plated Bangles", 249, "Accessories", "Bangles",
     "Elegant gold-plated bangles for festive and everyday styling.",
     "Metal", "Embellished"),

    ("Printed Silk Scarf", 299, "Accessories", "Scarf",
     "Colourful printed scarf.",
     "Silk Blend", "Printed"),

    ("Beige Bucket Hat", 249, "Accessories", "Cap / Hat",
     "Casual beige bucket hat.",
     "Cotton", "Solid"),

    ("Pearl Hair Accessories", 199, "Accessories", "Hair Accessories",
     "Pretty pearl hair accessories.",
     "Synthetic", "Pearl"),


    # =====================================================
    # FOOTWEAR
    # =====================================================

    ("White Casual Sneakers", 699, "Footwear", "Sneakers",
     "Classic white casual sneakers.",
     "Synthetic", "Solid"),

    ("Black Block Heels", 799, "Footwear", "Heels",
     "Elegant black block heels.",
     "Faux Leather", "Solid"),

    ("Beige Ballet Flats", 449, "Footwear", "Flats",
     "Comfortable beige ballet flats.",
     "Faux Leather", "Solid"),

    ("White Platform Sandals", 499, "Footwear", "Sandals",
     "Stylish white platform sandals.",
     "Synthetic", "Solid"),

    ("Black Ankle Boots", 899, "Footwear", "Boots",
     "Classic black ankle boots.",
     "Faux Leather", "Solid"),

    ("Brown Loafers", 649, "Footwear", "Loafers",
     "Classic brown loafers.",
     "Faux Leather", "Solid"),

    ("Black Mules", 549, "Footwear", "Mules",
     "Minimal black mules.",
     "Faux Leather", "Solid"),

    ("Beige Wedges", 699, "Footwear", "Wedges",
     "Comfortable beige wedges.",
     "Faux Leather", "Solid"),

    ("White Slides", 299, "Footwear", "Slides",
     "Casual white slides.",
     "Synthetic", "Solid"),

    ("Embroidered Juttis", 499, "Footwear", "Juttis",
     "Traditional embroidered juttis.",
     "Textile", "Embroidered")
]


connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()


# Make sure subcategory exists
columns = cursor.execute(
    "PRAGMA table_info(products)"
).fetchall()

column_names = [column[1] for column in columns]

if "subcategory" not in column_names:
    cursor.execute(
        "ALTER TABLE products ADD COLUMN subcategory TEXT"
    )


added = 0


for product in products:

    name = product[0]

    existing = cursor.execute(
        "SELECT id FROM products WHERE name = ?",
        (name,)
    ).fetchone()

    if existing:
        continue


    cursor.execute(
        """
        INSERT INTO products
        (
            name,
            price,
            category,
            subcategory,
            description,
            fabric,
            pattern
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        product
    )

    added += 1


connection.commit()
connection.close()


print()
print("========================================")
print("ReWear catalogue updated! ♻️")
print("New products added:", added)
print("Total products:", len(products))
print("========================================")