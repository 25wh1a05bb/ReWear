import os
import sqlite3
import urllib.request
import urllib.parse
import json


DATABASE = "rewear.db"

CATALOG_FOLDER = os.path.join("static", "catalog")

os.makedirs(CATALOG_FOLDER, exist_ok=True)


# ---------------------------------------------------------
# IMAGE SEARCH TERMS
# ---------------------------------------------------------

IMAGE_SEARCHES = {

    "bodycon.jpg": "black bodycon dress",

    "maxi_dress.jpg": "floral maxi dress",

    "crop_top.jpg": "women crop top",

    "halter_top.jpg": "women halter top",

    "jeans.jpg": "women blue jeans",

    "saree.jpg": "Indian saree",

    "denim_jacket.jpg": "women denim jacket",

    "blazer.jpg": "women blazer",

    "handbag.jpg": "women handbag",

    "bangles.jpg": "gold bangles",

    "sneakers.jpg": "women sneakers",

    "sandals.jpg": "women sandals",

    "heels.jpg": "women high heels",

}


# ---------------------------------------------------------
# WIKIMEDIA COMMONS SEARCH
# ---------------------------------------------------------

def search_wikimedia(search_term):

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": search_term,
        "gsrnamespace": "6",
        "gsrlimit": "10",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata",
        "iiurlwidth": "800",
        "format": "json",
        "origin": "*"
    }

    url = (
        "https://commons.wikimedia.org/w/api.php?"
        + urllib.parse.urlencode(params)
    )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ReWear-MVP/1.0"
        }
    )

    with urllib.request.urlopen(request, timeout=30) as response:

        data = json.loads(
            response.read().decode("utf-8")
        )

    pages = data.get("query", {}).get("pages", {})

    for page in pages.values():

        imageinfo = page.get("imageinfo")

        if not imageinfo:
            continue

        info = imageinfo[0]

        image_url = info.get("thumburl") or info.get("url")

        metadata = info.get("extmetadata", {})

        license_name = metadata.get(
            "LicenseShortName",
            {}
        ).get("value", "")

        artist = metadata.get(
            "Artist",
            {}
        ).get("value", "")

        page_url = (
            "https://commons.wikimedia.org/wiki?"
            + urllib.parse.urlencode({
                "curid": page["pageid"]
            })
        )

        return {
            "image_url": image_url,
            "page_url": page_url,
            "license": license_name,
            "artist": artist,
            "title": page.get("title", "")
        }

    return None


# ---------------------------------------------------------
# DOWNLOAD IMAGES
# ---------------------------------------------------------

credits = {}

print()
print("========================================")
print("ReWear catalogue image setup")
print("Searching Wikimedia Commons...")
print("========================================")
print()


for filename, search_term in IMAGE_SEARCHES.items():

    filepath = os.path.join(
        CATALOG_FOLDER,
        filename
    )

    print("Searching:", search_term)

    try:

        result = search_wikimedia(search_term)

        if not result:

            print("No image found:", search_term)
            print()
            continue


        request = urllib.request.Request(
            result["image_url"],
            headers={
                "User-Agent": "ReWear-MVP/1.0"
            }
        )


        with urllib.request.urlopen(
            request,
            timeout=30
        ) as response:

            image_data = response.read()


        with open(filepath, "wb") as file:

            file.write(image_data)


        credits[filename] = result


        print("Downloaded:", filename)
        print("License:", result["license"])
        print()


    except Exception as error:

        print("FAILED:", filename)
        print(error)
        print()


# ---------------------------------------------------------
# SAVE IMAGE CREDITS
# ---------------------------------------------------------

credits_file = os.path.join(
    CATALOG_FOLDER,
    "image_credits.json"
)


with open(
    credits_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        credits,
        file,
        indent=4,
        ensure_ascii=False
    )


# ---------------------------------------------------------
# PRODUCT → IMAGE MATCHING
# ---------------------------------------------------------

def choose_image(name, category, subcategory):

    text = " ".join([
        str(name or ""),
        str(category or ""),
        str(subcategory or "")
    ]).lower()


    # DRESSES

    if "bodycon" in text:
        return "bodycon.jpg"

    if "maxi" in text or "floral" in text:
        return "maxi_dress.jpg"

    if "dress" in text:
        return "maxi_dress.jpg"


    # TOPS

    if "halter" in text:
        return "halter_top.jpg"

    if "crop" in text:
        return "crop_top.jpg"

    if "top" in text or "shirt" in text:
        return "crop_top.jpg"


    # JEANS / BOTTOMWEAR

    if "jeans" in text:
        return "jeans.jpg"

    if any(word in text for word in [
        "wide leg",
        "straight fit",
        "skinny",
        "slim fit",
        "mom fit",
        "boyfriend",
        "baggy",
        "bootcut",
        "flared"
    ]):
        return "jeans.jpg"


    # ETHNIC

    if any(word in text for word in [
        "saree",
        "sari",
        "kurti",
        "anarkali",
        "lehenga",
        "salwar",
        "sharara",
        "ethnic"
    ]):
        return "saree.jpg"


    # OUTERWEAR

    if "denim" in text and "jacket" in text:
        return "denim_jacket.jpg"

    if "blazer" in text:
        return "blazer.jpg"

    if any(word in text for word in [
        "jacket",
        "coat",
        "cardigan",
        "shrug",
        "bomber",
        "trench",
        "hoodie",
        "sweatshirt"
    ]):
        return "denim_jacket.jpg"


    # ACCESSORIES

    if "bangle" in text:
        return "bangles.jpg"

    if any(word in text for word in [
        "handbag",
        "shoulder bag",
        "crossbody",
        "tote",
        "clutch",
        "backpack",
        "purse",
        "wallet"
    ]):
        return "handbag.jpg"


    # FOOTWEAR

    if "sneaker" in text:
        return "sneakers.jpg"

    if any(word in text for word in [
        "heel",
        "heels",
        "wedge"
    ]):
        return "heels.jpg"

    if any(word in text for word in [
        "sandal",
        "flat",
        "mule",
        "slide",
        "loafer"
    ]):
        return "sandals.jpg"


    # CATEGORY FALLBACKS

    if "accessories" in text:
        return "handbag.jpg"

    if "footwear" in text:
        return "sneakers.jpg"

    if "bottomwear" in text:
        return "jeans.jpg"

    if "outerwear" in text:
        return "denim_jacket.jpg"


    return "maxi_dress.jpg"


# ---------------------------------------------------------
# UPDATE DATABASE
# ---------------------------------------------------------

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()


products = cursor.execute("""
    SELECT id, name, category, subcategory
    FROM products
""").fetchall()


updated = 0


for product_id, name, category, subcategory in products:

    image_name = choose_image(
        name,
        category,
        subcategory
    )


    image_path = os.path.join(
        CATALOG_FOLDER,
        image_name
    )


    if os.path.exists(image_path):

        cursor.execute("""
            UPDATE products
            SET image1 = ?
            WHERE id = ?
        """, (
            image_name,
            product_id
        ))

        updated += 1


connection.commit()
connection.close()


print()
print("========================================")
print("ReWear catalogue setup complete! ♻️")
print("Products updated:", updated)
print("========================================")
print()