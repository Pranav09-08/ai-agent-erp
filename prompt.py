from datetime import datetime, timedelta

def get_dates():
    current_date = datetime.now()
    valid_till = current_date + timedelta(days=3)

    return {
        "current_date": current_date.strftime("%d %b %Y %I:%M %p"),
        "valid_till": valid_till.strftime("%d %b %Y")
    }


def build_prompt(data):
    items_table = ""
    dates = get_dates()
    
    for item in data.items:
        items_table += (
    f"| {item.name} | {item.model or '-'} | {item.description or '-'} "
    f"| {item.quantity} | {item.unitPrice} "
    f"| {item.standardDiscount} | {item.additionalDiscount} "
    f"| {item.taxableAmount} |\n"
)




    return f"""
You are a professional B2B sales executive preparing a **GST-compliant Indian business quotation**.

Generate a **FORMAL BUSINESS QUOTATION** using the exact structure below.
Use ONLY the data provided. Do NOT modify prices, discounts, taxes, or quantities.

### FORMAT RULES (MANDATORY)
- Use Markdown
- Maintain clear section separation
- Use tables exactly as defined
- Do NOT add assumptions, offers, or extra terms
- Currency: {data.currency}
- Tone: Professional, precise, corporate  
- Valid Till : {data.validTill} just take the date, no time from this field
- Vali Till date should be 3 days from the current date
- Take current date as my system correct date
 
---

# QUOTATION

| **From (Seller)** | **To (Client)** |
|------------------|----------------|
| **{data.sender.companyName}** | **{data.client.companyName}** |
| {data.sender.address} | {data.client.address} |
| GSTIN: {data.sender.gstin} | GSTIN: {data.client.gstin} |
| Email: {data.sender.email} | Email: {data.client.email} |


---

**Quotation Reference:** Q-{data.quotationId}  
**Date:** {dates["current_date"]}  
**Valid Till:** {dates["valid_till"]}

---

## ORDER SUMMARY

| Item     | Model | Description | Qty | Unit Price ({data.currency}) | Standard Discount | Additional Discount | Line Total ({data.currency}) |
|----------|-------|-------------|-----|-------------------------------|-------------------|---------------------|-------------------------------|
{items_table}

---

## PRICING & TAX SUMMARY

| Description | Amount ({data.currency}) |
|------------|--------------------------|
| Subtotal | {data.pricing.subtotal} |
| CGST ({data.pricing.cgstPercent}%) | {data.pricing.cgst} |
| SGST ({data.pricing.sgstPercent}%) | {data.pricing.sgst} |
| **Total Payable** | **{data.pricing.total}** |
|**Amount in Words:** | *{data.pricing.totalInWords}*|


---

## TERMS & CONDITIONS
- This quotation is valid until the date mentioned above.
- Prices are exclusive of any other statutory levies unless stated.
- Taxes are applied as per prevailing GST regulations.
- Payment terms as per standard company policy.

---

## AUTHORIZED SIGNATORY

**Sales Manager:** {data.salesManager.name}
**Email:** {data.salesManager.email}

---

End the quotation with a professional closing statement suitable for a corporate client.
"""
