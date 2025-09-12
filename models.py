from pydantic import BaseModel
from datetime import datetime

class Customer(BaseModel):
    id: str
    name: str
    description: str | None = None
    email: str
    age: int

class Transaction(BaseModel):
    id: str
    amount: int # in cents
    currency: str
    timestamp: datetime
    customer_id: str

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int = 0

    @property
    def total(self):
        return sum(t.amount for t in self.transactions)
