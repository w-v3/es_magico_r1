from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from db_setup.db_setup import ProductSKU, ProductListing, engine
from typing import List, Optional

app = FastAPI()
engine = create_engine('sqlite:///db_setup/local.db')
SessionLocal = sessionmaker(bind=engine)

# Response Models
class PriceUnit(BaseModel):
    value: float
    unit: str

class DimensionsUnit(BaseModel):
    unit: str
    length: float
    width: float
    height: float

class MarketplaceEntry(BaseModel):
    status: str
    marketplace: str

class ProductSKUResponse(BaseModel):
    parentage: Optional[str]
    mfn_sku: str
    sku_name: str
    country: Optional[str] = None
    epic_purchase_cost: Optional[PriceUnit]
    contracted_sell_price: Optional[PriceUnit]
    case_quantity: Optional[int]
    upc_gtin: Optional[str]
    retail_price: Optional[PriceUnit]
    asin: Optional[str]
    lead_time: Optional[int]
    weight: Optional[PriceUnit]
    dimensions: Optional[DimensionsUnit]
    packaging_weight: Optional[PriceUnit] = None
    packaging_dimensions: Optional[DimensionsUnit] = None
    marketplaces: List[MarketplaceEntry] = []

class SKUListResponse(BaseModel):
    sku: List[ProductSKUResponse]

# Helper to convert raw DB JSON -> typed API object

def extract_unit_data(json_obj, default_unit="unit"):
    if not json_obj:
        return None
    return {
        "value": json_obj.get("value"),
        "unit": json_obj.get("currency", json_obj.get("unit", default_unit))
    }

def extract_dimensions(json_obj):
    if not json_obj:
        return None
    return {
        "unit": json_obj.get("unit", "unit"),
        "length": json_obj.get("length"),
        "width": json_obj.get("width"),
        "height": json_obj.get("height")
    }

@app.get("/skus", response_model=SKUListResponse)
def get_skus(skip: int = Query(0, ge=0), limit: int = Query(10, le=50)):
    db = SessionLocal()
    try:
        skus = db.query(ProductSKU).options(joinedload(ProductSKU.product_listings)).offset(skip).limit(limit).all()
        
        print(len(skus))
        results = []
        for sku in skus:
            listings = [
                MarketplaceEntry(status=l.status.value, marketplace=l.marketplace.value)
                for l in sku.product_listings
            ]

            results.append(ProductSKUResponse(
                parentage=sku.parentage,
                mfn_sku=sku.mfn_sku,
                sku_name=sku.name,
                country=sku.product_listings[0].country if sku.product_listings else None,
                epic_purchase_cost=extract_unit_data(sku.epic_purchase_cost),
                contracted_sell_price=extract_unit_data(sku.contracted_sell_price),
                case_quantity=sku.case_quantity,
                upc_gtin=sku.upc_gtin,
                retail_price=extract_unit_data(sku.retail_price),
                asin=sku.asin,
                lead_time=sku.lead_time.get("days") if sku.lead_time else None,
                weight=extract_unit_data(sku.weight),
                dimensions=extract_dimensions(sku.dimensions),
                packaging_weight=extract_unit_data(sku.weight),  # assuming same as weight for now
                packaging_dimensions=extract_dimensions(sku.dimensions),  # assuming same as dimensions
                marketplaces=listings
            ))

        return {"sku": results}

    finally:
        db.close()
