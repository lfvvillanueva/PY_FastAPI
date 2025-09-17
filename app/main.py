from fastapi import FastAPI, HTTPException, status

from models import CustomerBase, Customer, Transaction, Invoice, CustomerUpdate

from database import SessionDep, create_all_tables

from sqlmodel import select

from datetime import datetime

from .routers import customers

import zoneinfo

app = FastAPI(lifespan=create_all_tables)

app.include_router(customers.router)

@app.get("/")
async def read_root():
    return {"Hello Luis Venegas"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str =country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}

db_customers : list[Customer] = []

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data