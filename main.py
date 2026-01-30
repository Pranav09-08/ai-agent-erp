from fastapi import FastAPI, HTTPException
from schemas import QuotationInput, QuotationOutput
from prompt import build_prompt
from dotenv import load_dotenv
import os
from groq import Groq
import traceback

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

app = FastAPI()

@app.post("/generate-quotation", response_model=QuotationOutput)
def generate_quotation(data: QuotationInput):
    try:
        prompt = build_prompt(data)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional B2B sales executive."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return {
            "subject": f"Quotation #{data.quotationId} – {data.client.companyName}",
            "body": response.choices[0].message.content
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
