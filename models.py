from pydantic import BaseModel, EmailStr
from datetime import datetime
from sqlmodel import SQLModel, Field

#https://docs.pydantic.dev/latest//usage/models/

class CustomerBase(SQLModel):
    name: str
    description: str | None = None
    email: str
    age: int
    email: EmailStr # Email validation

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  

class Transaction(BaseModel):
    id: str
    amount: int # in cents
    currency: str
    timestamp: datetime
    customer_id: str

class Invoice(BaseModel):
    id: int
    customer: CustomerBase
    transactions: list[Transaction]
    total: int = 0

    @property
    def total(self):
        return sum(t.amount for t in self.transactions)
