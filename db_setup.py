from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Enum, JSON, ForeignKey, TIMESTAMP, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

# Enums
class AccountStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    deleted = "deleted"

class ProductSkuStatus(enum.Enum):
    available = "available"
    out_of_stock = "out_of_stock"
    discontinued = "discontinued"
    archived = "archived"

class ProductListingStatus(enum.Enum):
    pending = "pending"
    live = "live"
    paused = "paused"
    terminated = "terminated"
    deleted = "deleted"
    queued = "queued"
    draft = "draft"

class Marketplaces(enum.Enum):
    mercado_libre = "mercado_libre"
    lazada = "lazada"
    shopee = "shopee"
    rakuten = "rakuten"
    coupang = "coupang"
    walmart = "walmart"
    amazon = "amazon"

# Tables
class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String)
    onboarded_at = Column(TIMESTAMP)
    profile_pic_url = Column(String)
    status = Column(Enum(AccountStatus), nullable=False, default=AccountStatus.inactive)
    extra_metadata = Column(JSON)  # renamed from metadata

    product_skus = relationship("ProductSKU", back_populates="brand")


class ProductSKU(Base):
    __tablename__ = 'product_sku'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    product_url = Column(String)
    parentage = Column(String)
    name = Column(String)
    mfn_sku = Column(String, unique=True)
    case_quantity = Column(Integer)
    upc_gtin = Column(String)
    asin = Column(String)
    epic_purchase_cost = Column(JSON)
    contracted_sell_price = Column(JSON)
    retail_price = Column(JSON)
    lead_time = Column(JSON)
    weight = Column(JSON)
    dimensions = Column(JSON)
    status = Column(Enum(ProductSkuStatus), nullable=False, default=ProductSkuStatus.available)
    extra_metadata = Column(JSON)  # renamed from metadata
    is_active = Column(Boolean, nullable=False, default=True)

    brand = relationship("Brand", back_populates="product_skus")
    product_listings = relationship("ProductListing", back_populates="product_sku")


class ProductListing(Base):
    __tablename__ = 'product_listing'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    epic_sku_id = Column(String, unique=True, nullable=False)
    product_sku_id = Column(Integer, ForeignKey('product_sku.id'))
    marketplace = Column(Enum(Marketplaces), nullable=False)
    country = Column(String)
    status = Column(Enum(ProductListingStatus), nullable=False, default=ProductListingStatus.pending)
    epic_status = Column(String)
    extra_metadata = Column(JSON)  # renamed from metadata

    __table_args__ = (
        UniqueConstraint('product_sku_id', 'marketplace', 'country', name='unique_product_sku_id_marketplace_profile_id'),
    )

    product_sku = relationship("ProductSKU", back_populates="product_listings")

# Initialize SQLite DB
engine = create_engine('sqlite:///local.db')
Base.metadata.create_all(engine)

print("✅ SQLite DB setup complete.")
