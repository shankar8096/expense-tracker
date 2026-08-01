from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Expense(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    date: str


expenses_db: List[Expense] = []


@app.get("/")
def home():
    return {"message": "Smart Expense Tracker API is Live!"}


@app.post("/expenses", response_model=Expense)
def add_expense(expense: Expense):
    for item in expenses_db:
        if item.id == expense.id:
            raise HTTPException(
                status_code=400, detail="Expense ID already exists"
            )
    expenses_db.append(expense)
    return expense


@app.get("/expenses", response_model=List[Expense])
def get_expenses(category: Optional[str] = None):
    if category:
        filtered = [
            e for e in expenses_db if e.category.lower() == category.lower()
        ]
        return filtered
    return expenses_db


@app.get("/expenses/total")
def get_total_expenses(category: Optional[str] = None):
    if category:
        total = sum(
            e.amount
            for e in expenses_db
            if e.category.lower() == category.lower()
        )
        return {"category": category, "total": total}
    total = sum(e.amount for e in expenses_db)
    return {"overall_total": total}


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    for index, expense in enumerate(expenses_db):
        if expense.id == expense_id:
            deleted = expenses_db.pop(index)
            return {"message": "Expense deleted", "deleted_expense": deleted}
    raise HTTPException(status_code=404, detail="Expense not found")
