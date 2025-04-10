from sqlalchemy.orm import sessionmaker
from db_setup import engine, ProductSKU, ProductListing

Session = sessionmaker(bind=engine)
session = Session()

# --- Insert 10 Product SKUs ---
product_skus = [
    ProductSKU(
        brand_id=1,
        product_url=f"https://nike.com/item-{i}",
        parentage="child" if i % 2 == 0 else "parent",
        name=f"Nike Product {i}",
        mfn_sku=f"NIKE-{i:03d}",
        case_quantity=10 + i,
        upc_gtin=f"1234567890{i:02d}",
        asin=f"B000NIKE{i:03d}",
        epic_purchase_cost={"value": 70 + i, "currency": "USD"},
        contracted_sell_price={"value": 100 + i, "currency": "USD"},
        retail_price={"value": 120 + i, "currency": "USD"},
        lead_time={"days": 5 + i % 3},
        weight={"value": 1.0 + (i * 0.1), "unit": "kg"},
        dimensions={"length": 30+i, "width": 20+i, "height": 10+i, "unit": "cm"},
        status="available" if i % 3 else "out_of_stock"
    ) for i in range(1, 6)
] + [
    ProductSKU(
        brand_id=2,
        product_url=f"https://adidas.com/item-{i}",
        parentage="child" if i % 2 == 0 else "parent",
        name=f"Adidas Product {i}",
        mfn_sku=f"ADIDAS-{i:03d}",
        case_quantity=5 + i,
        upc_gtin=f"9876543210{i:02d}",
        asin=f"B000ADIDAS{i:03d}",
        epic_purchase_cost={"value": 75 + i, "currency": "USD"},
        contracted_sell_price={"value": 105 + i, "currency": "USD"},
        retail_price={"value": 125 + i, "currency": "USD"},
        lead_time={"days": 4 + i % 3},
        weight={"value": 0.9 + (i * 0.1), "unit": "kg"},
        dimensions={"length": 28+i, "width": 18+i, "height": 9+i, "unit": "cm"},
        status="available" if i % 2 else "discontinued"
    ) for i in range(6, 11)
]

session.add_all(product_skus)
session.commit()

# --- Insert 10 Product Listings ---
marketplace_country_pairs = [
    ("amazon", "US"),
    ("shopee", "SG"),
    ("lazada", "MY"),
    ("rakuten", "JP"),
    ("coupang", "KR"),
    ("walmart", "US"),
    ("mercado_libre", "AR"),
    ("amazon", "CA"),
    ("shopee", "PH"),
    ("rakuten", "JP"),
]

product_listings = [
    ProductListing(
        epic_sku_id=f"SKU-{1000 + i}",
        product_sku_id=i + 1,
        marketplace=marketplace_country_pairs[i][0],
        country=marketplace_country_pairs[i][1],
        status=["pending", "live", "paused", "queued", "deleted", "draft", "terminated"][i % 7],
        epic_status="synced" if i % 2 else "awaiting_approval"
    ) for i in range(10)
]

session.add_all(product_listings)
session.commit()

print("✅ 10 more SKUs and Listings added successfully!")
