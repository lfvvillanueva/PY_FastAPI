from fastapi import FastAPI

from Models.models import CustomerBase, Customer, Transaction, Invoice

from DB.database import SessionDep, create_all_tables

from sqlmodel import select

import zoneinfo

app = FastAPI(lifespan=create_all_tables)

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

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerBase, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@app.get('/customers/{customer_id}', response_model=Customer)
async def get_customer(customer_id: int):
    customer = next((c for c in db_customers if c.id == customer_id), None)
    if not customer:
        return {"error": "Customer not found"}
    return customer

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data