from models import Customer, CustomerBase, CustomerUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from database import SessionDep

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerBase, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}", response_model=Customer)
async def read_customers(customer_id: int, session: SessionDep):
    db_customers = session.get(Customer, customer_id)
    if not db_customers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return db_customers

@router.delete("/customers/{customer_id}")
async def delete_customers(customer_id: int, session: SessionDep):
    db_customers = session.get(Customer, customer_id)
    if not db_customers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(db_customers)
    session.commit()
    return {"detail": "Customer deleted"}

@router.patch("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def read_customer(
    customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exits")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.get("/customers", response_model=list[Customer])
async def list_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.get('/customers/{customer_id}', response_model=Customer)
async def get_customer(customer_id: int):
    customer = next((c for c in db_customers if c.id == customer_id), None)
    if not customer:
        return {"error": "Customer not found"}
    return customer