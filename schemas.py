from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# ---------- Line Item ----------

class Item(BaseModel):
    name: str
    model: Optional[str] = None
    description: Optional[str] = None
    quantity: int

    unitPrice: float

    standardDiscount: Optional[float] = 0
    additionalDiscount: Optional[float] = 0

    cgstPercent: Optional[float] = None
    sgstPercent: Optional[float] = None

    taxableAmount : Optional[float] = None

    lineTotal: float


# ---------- Pricing ----------

class Pricing(BaseModel):
    subtotal: float
    cgst: float
    sgst: float

    cgstPercent: Optional[float] = None
    sgstPercent: Optional[float] = None

    total: float
    totalInWords: Optional[str] = None


# ---------- Party Info ----------

class Company(BaseModel):
    companyName: str
    address: Optional[str] = None
    gstin: Optional[str] = None
    email: Optional[str] = None


class SalesManager(BaseModel):
    name: str
    email: str


# ---------- Quotation ----------

class QuotationInput(BaseModel):
    quotationId: str            # 🔥 FIXED (Firebase-safe)
    sender: Company
    client: Company
    salesManager: SalesManager
    items: List[Item]
    pricing: Pricing
    validTill: datetime         # 🔥 Better than plain string
    currency: str


# ---------- AI Output ----------

class QuotationOutput(BaseModel):
    subject: str
    body: str
