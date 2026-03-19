from fastapi import FastAPI, HTTPException
from app.models import OrderCreate, Order, OrderUpdateStatus, Pricing, PricingUpdate, OrderStatus
from app.db import get_connection, init_db, DB_PATH
from datetime import datetime, timezone

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    if not DB_PATH.is_file():
        print('Initializing DB...')
        init_db()

    yield

app = FastAPI(lifespan=lifespan)

# Helper: get price per page
def get_price(print_type: str) -> float:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT price_per_page FROM pricing WHERE print_type = ?", (print_type,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row["price_per_page"]
    else:
        raise HTTPException(status_code=400, detail="Print type not found in pricing table.")

@app.post("/orders", response_model=Order)
def create_order(order: OrderCreate):
    price = get_price(order.print_type)
    cost = price * order.pages
    now = datetime.now(timezone.utc).isoformat()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (customer_name, pages, print_type, cost, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (order.customer_name, order.pages, order.print_type, cost, OrderStatus.pending.value, now, now)
    )
    order_id = cur.lastrowid
    conn.commit()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cur.fetchone()
    conn.close()
    return Order(**row)

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return Order(**row)
    else:
        raise HTTPException(status_code=404, detail="Order not found.")

@app.get("/orders", response_model=list[Order])
def list_orders(status: OrderStatus | None = None):
    conn = get_connection()
    cur = conn.cursor()
    if status:
        cur.execute("SELECT * FROM orders WHERE status = ? ORDER BY created_at", (status.value,))
    else:
        cur.execute("SELECT * FROM orders ORDER BY created_at")
    rows = cur.fetchall()
    conn.close()
    return [Order(**row) for row in rows]

@app.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: int, update: OrderUpdateStatus):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found.")
    cur.execute(
        "UPDATE orders SET status = ?, updated_at = ? WHERE id = ?",
        (update.status.value, datetime.now(timezone.utc).isoformat(), order_id)
    )
    conn.commit()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    updated_row = cur.fetchone()
    conn.close()
    return Order(**updated_row)

@app.delete("/orders/{order_id}", response_model=dict)
def cancel_order(order_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found.")
    cur.execute(
        "UPDATE orders SET status = ?, updated_at = ? WHERE id = ?",
        (OrderStatus.cancelled.value, datetime.now(timezone.utc).isoformat(), order_id)
    )
    conn.commit()
    conn.close()
    return {"detail": "Order cancelled."}

@app.get("/pricing", response_model=list[Pricing])
def get_pricing():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pricing ORDER BY print_type")
    rows = cur.fetchall()
    conn.close()
    return [Pricing(**row) for row in rows]

@app.put("/pricing/{print_type}", response_model=Pricing)
def update_pricing(print_type: str, update: PricingUpdate):
    now = datetime.now(timezone.utc).isoformat()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pricing WHERE print_type = ?", (print_type,))
    row = cur.fetchone()
    if row:
        cur.execute(
            "UPDATE pricing SET price_per_page = ?, updated_at = ? WHERE print_type = ?",
            (update.price_per_page, now, print_type)
        )
    else:
        cur.execute(
            "INSERT INTO pricing (print_type, price_per_page, updated_at) VALUES (?, ?, ?)",
            (print_type, update.price_per_page, now)
        )
    conn.commit()
    cur.execute("SELECT * FROM pricing WHERE print_type = ?", (print_type,))
    updated_row = cur.fetchone()
    conn.close()
    return Pricing(**updated_row)
