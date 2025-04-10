from sqlalchemy.orm import sessionmaker
from db_setup import engine, Brand, ProductSKU, ProductListing
import datetime

Session = sessionmaker(bind=engine)
session = Session()

# 1. Insert Brands
brands = [
    Brand(
        name="Nike",
        onboarded_at=datetime.datetime(2023, 1, 1, 12, 0),
        profile_pic_url="https://example.com/nike.jpg",
        status="active"
    ),
    Brand(
        name="Adidas",
        onboarded_at=datetime.datetime(2023, 2, 15, 15, 30),
        profile_pic_url="https://example.com/adidas.jpg",
        status="active"
    )
]

session.add_all(brands)
session.commit()

# 2. Insert Product SKUs
product_skus = [
    ProductSKU(
        brand_id=1,
        product_url="https://nike.com/shoe-123",
        parentage="parent",
        name="Nike Air Max",
        mfn_sku="NIKE-AM-001",
        case_quantity=10,
        upc_gtin="123456789012",
        asin="B000123NIKE",
        epic_purchase_cost={"value": 80.0, "currency": "USD"},
        contracted_sell_price={"value": 110.0, "currency": "USD"},
        retail_price={"value": 130.0, "currency": "USD"},
        lead_time={"days": 5},
        weight={"value": 1.2, "unit": "kg"},
        dimensions={"length": 30, "width": 20, "height": 10, "unit": "cm"},
        status="available"
    ),
    ProductSKU(
        brand_id=2,
        product_url="https://adidas.com/shoe-abc",
        parentage="parent",
        name="Adidas Ultraboost",
        mfn_sku="ADIDAS-UB-002",
        case_quantity=8,
        upc_gtin="987654321098",
        asin="B000321ADIDAS",
        epic_purchase_cost={"value": 90.0, "currency": "USD"},
        contracted_sell_price={"value": 120.0, "currency": "USD"},
        retail_price={"value": 150.0, "currency": "USD"},
        lead_time={"days": 7},
        weight={"value": 1.0, "unit": "kg"},
        dimensions={"length": 32, "width": 22, "height": 12, "unit": "cm"},
        status="available"
    )
]

session.add_all(product_skus)
session.commit()

# 3. Insert Product Listings
product_listings = [
    ProductListing(
        epic_sku_id="NIKE-AM-001-USA-AMZ",
        product_sku_id=1,
        marketplace="amazon",
        country="US",
        status="live",
        epic_status="synced"
    ),
    ProductListing(
        epic_sku_id="ADIDAS-UB-002-SG-SHP",
        product_sku_id=2,
        marketplace="shopee",
        country="SG",
        status="pending",
        epic_status="awaiting_approval"
    )
]

session.add_all(product_listings)
session.commit()

print("✅ Seed data inserted successfully!")
