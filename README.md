# FastPrint API

## About
FastPrint is a FastAPI application for managing print orders and cost calculation in a campus printing shop. It replaces manual order tracking and computation with a modern API, using a file-based SQLite database. The app supports order creation, status updates, pricing management, and record retrieval.

### Features
- Record print orders automatically
- Compute total cost per order
- Update and track order status (queued, pending, cancelled, finished)
- Manage pricing for print types
- Retrieve single/multiple order records

## API Endpoints

### Orders
- `POST /orders` — Create a new print order
- `GET /orders/{order_id}` — Retrieve a single order by ID
- `GET /orders` — List all orders (optionally filter by status)
- `PATCH /orders/{order_id}/status` — Update order status
- `DELETE /orders/{order_id}` — Cancel an order

### Pricing
- `GET /pricing` — List all pricing entries
- `PUT /pricing/{print_type}` — Update or add pricing for a print type

## Order Status Values
- queued
- pending
- cancelled
- finished

## Database
- Uses SQLite file `fastprint.db` at project root

## How to Run

1. **Install dependencies**
   - Create and activate a virtual environment:
     - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
     - Linux: `python3 -m venv .venv` then `source .venv\Scripts\activate`
   - Install requirements:
     - `pip install -r requirements.txt`

2. **Start the API server**
   - Run:
     - `uvicorn app.main:app --reload`

3. **Access the API docs**
   - Open your browser at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Notes
- All endpoints return JSON responses
- Pricing must be set before creating orders for new print types
- Database tables are auto-created on startup

---
For questions or issues, contact the developer or open an issue.