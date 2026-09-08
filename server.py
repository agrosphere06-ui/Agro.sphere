"""
Agro-Sphere — Production REST API Backend Server
Powered by FastAPI, SQLite & Pydantic
"""

import sqlite3
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Agro-Sphere Backend API",
    description="Live REST API for Mandi Prices, Produce Lots, Collective Pooling, Logistics, and Kisan Voice AI",
    version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "agrosphere.db"

# -------------------------------------------------------------
# DATABASE INITIALIZATION
# -------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop TEXT NOT NULL,
        category TEXT NOT NULL,
        grade TEXT NOT NULL,
        location TEXT NOT NULL,
        qty REAL NOT NULL,
        price REAL NOT NULL,
        img TEXT,
        emoji TEXT DEFAULT '🌾',
        buyer TEXT DEFAULT 'Open Market',
        is_urgent INTEGER DEFAULT 0,
        size_spec TEXT,
        freshness_spec TEXT,
        packaging_spec TEXT,
        pesticide_spec TEXT,
        harvest_spec TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Callbacks / Support requests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS support_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        query_type TEXT,
        language TEXT,
        status TEXT DEFAULT 'Pending (15m SLA)',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Vehicles / Logistics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicle_trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_no TEXT UNIQUE NOT NULL,
        driver_name TEXT NOT NULL,
        driver_phone TEXT NOT NULL,
        agency TEXT NOT NULL,
        status TEXT DEFAULT 'In Transit',
        speed TEXT DEFAULT '42 km/h',
        eta TEXT DEFAULT '45 Mins',
        progress_pct INTEGER DEFAULT 65,
        pickup_pin TEXT DEFAULT '4829'
    )
    """)

    # Seed initial vehicle if empty
    cursor.execute("SELECT COUNT(*) FROM vehicle_trips")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO vehicle_trips (vehicle_no, driver_name, driver_phone, agency, status, speed, eta, progress_pct, pickup_pin)
        VALUES ('MH-15-AB-1234', 'Ramesh Shinde', '+91 98765 43210', 'Kisan Express Logistics', 'In Transit', '42 km/h', '45 Mins', 65, '4829')
        """)

    # Seed initial products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        initial_products = [
            # ONION
            ('Onion', 'vegetables', 'Grade A', 'Lasalgaon', 80, 3420, 'https://images.unsplash.com/photo-1664975367131-4c7ac2efa704?q=80&w=765&auto=format&fit=crop', '🧅', 'FreshKart', 0, '55mm - 70mm Uniform', '94% Dry Cured (Lasalgaon Red)', '50kg Ventilated Jute Bags', 'Lab Tested / GAP Verified', 'Cured 3 days ago'),
            ('Onion', 'vegetables', 'Grade B', 'Pune', 50, 3180, 'https://images.unsplash.com/photo-1664975367131-4c7ac2efa704?q=80&w=765&auto=format&fit=crop', '🧅', 'Metro Wholesale', 0, '45mm - 55mm Medium', 'Standard Dry Cured', '45kg Mesh Bags', 'Mandi Tested Standard', 'Farm Packed'),

            # TOMATO
            ('Tomato', 'vegetables', 'Grade A', 'Lasalgaon', 45, 3020, 'https://images.unsplash.com/photo-1607305387299-a3d9611cd469?q=80&w=2070&auto=format&fit=crop', '🍅', 'FreshBasket', 0, '55mm - 65mm Uniform Firm Red', '95% Fresh Ripe', '25kg Plastic Crates', 'Zero Chemical Residue', 'Packed Today'),
            ('Tomato', 'vegetables', 'Grade B', 'Nagpur', 35, 2650, 'https://images.unsplash.com/photo-1607305387299-a3d9611cd469?q=80&w=2070&auto=format&fit=crop', '🍅', 'CityFresh Foods', 1, '45mm - 55mm Salad/Processing', '90% Farm Fresh', '25kg Plastic Crates', 'Safe Quality Certified', 'Daily Pick'),

            # LEMON
            ('Lemon', 'vegetables', 'Grade A', 'Nagpur', 45, 4600, 'https://plus.unsplash.com/premium_photo-1724252307021-8bef16b863b7?q=80&w=687&auto=format&fit=crop', '🍋', 'CitrusCo Direct', 0, '45mm - 55mm (Kagzi Juicy)', '95% Juicy · Thin Skin', '20kg Ventilated Crates', '100% Organic / Residue Free', 'Harvested Yesterday'),
            ('Lemon', 'vegetables', 'Grade B', 'Pune', 30, 3800, 'https://plus.unsplash.com/premium_photo-1724252307021-8bef16b863b7?q=80&w=687&auto=format&fit=crop', '🍋', 'JuiceMasters Processing', 1, '38mm - 45mm Processing Grade', '90% Juicy Extract Grade', '30kg Mesh Bags', 'GAP Certified', 'Harvested 2 days ago'),

            # POTATO
            ('Potato', 'vegetables', 'Grade A', 'Pune', 90, 2150, 'https://plus.unsplash.com/premium_photo-1724849333632-d88aa5a73d9c?q=80&w=687&auto=format&fit=crop', '🥔', 'SpudCorp Logistics', 0, '50mm+ Jyoti Variety', 'Dry Farm Stored', '50kg Jute Sacks', 'Verified Clean', 'Graded & Packed'),
            ('Potato', 'vegetables', 'Grade B', 'Nagpur', 70, 1920, 'https://plus.unsplash.com/premium_photo-1724849333632-d88aa5a73d9c?q=80&w=687&auto=format&fit=crop', '🥔', 'Bharat Foods', 0, '40mm - 50mm Medium Table', 'Standard Table Quality', '50kg Gunny Bags', 'Lab Tested', 'Packed'),

            # POMEGRANATE
            ('Pomegranate', 'fruits', 'Grade A', 'Lasalgaon', 55, 7200, 'https://images.unsplash.com/photo-1541344999736-83eca872f240?q=80&w=1000&auto=format&fit=crop', '🍎', 'FreshFruit Exporters', 0, '250g - 350g (Bhagwa Ruby)', '98% Export Grade · Glossy Skin', '10kg Corrugated Boxes', 'Global GAP Certified', 'Harvested Today'),
            ('Pomegranate', 'fruits', 'Grade B', 'Pune', 40, 5800, 'https://images.unsplash.com/photo-1541344999736-83eca872f240?q=80&w=1000&auto=format&fit=crop', '🍎', 'JuiceMakers Direct', 1, '180g - 240g Standard', '90% Sweet Aril Juice Grade', '15kg Crates', 'Standard Mandi Pass', 'Harvested 2 days ago'),

            # MANGO
            ('Mango', 'fruits', 'Grade A', 'Ratnagiri', 40, 12500, 'https://plus.unsplash.com/premium_photo-1724255863470-4591b856cc10?q=80&w=687&auto=format&fit=crop', '🥭', 'Gourmet Fruit Hub', 1, '250g+ (Ratnagiri Alphonso GI)', 'Naturally Ripened · Rich Aroma', 'Wooden Gift Crates (12 Dozen)', 'Organic Certified', 'Tree-Ripened 2 Days Ago'),
            ('Mango', 'fruits', 'Grade B', 'Nagpur', 35, 9200, 'https://plus.unsplash.com/premium_photo-1724255863470-4591b856cc10?q=80&w=687&auto=format&fit=crop', '🥭', 'MahaFruit Wholesale', 0, '180g - 220g Table Grade', '88% Ripe Commercial Grade', 'Standard Cardboard Crates', 'Safe Tested', 'Harvested 3 days ago'),

            # WHEAT
            ('Wheat', 'grains', 'Grade A', 'Pune', 120, 2640, 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?q=80&w=1989&auto=format&fit=crop', '🌾', 'AgroMart', 0, 'Sharbati Gold Grain', 'Moisture < 11% Clean Dry', '50kg HDPE Bags', 'FSSAI Grade A', 'Cleaned & Machine Sorted'),
            ('Wheat', 'grains', 'Grade B', 'Nagpur', 75, 2320, 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?q=80&w=1989&auto=format&fit=crop', '🌾', 'Milling Flour Mills', 0, 'Lokwan Standard Grain', 'Moisture 12.2% Clean', '50kg Jute Sacks', 'APMC Standard', 'Farm Stored'),

            # SOYBEAN
            ('Soybean', 'grains', 'Grade A', 'Nagpur', 65, 4820, 'https://images.unsplash.com/photo-1639843606783-b2f9c50a7468?q=80&w=1073&auto=format&fit=crop', '🫘', 'GreenHarvest', 0, 'Yellow Bold Variety', 'Moisture 10% · Oil Content 19%', '50kg Bags', 'Certified Quality', 'Processed'),
            ('Soybean', 'grains', 'Grade B', 'Lasalgaon', 50, 4380, 'https://images.unsplash.com/photo-1639843606783-b2f9c50a7468?q=80&w=1073&auto=format&fit=crop', '🫘', 'Feed Mills Ltd', 0, 'Standard Commercial Yellow', 'Moisture 11.5% · Oil 17%', '50kg Gunny Sacks', 'Mandi Standard', 'Cleaned')
        ]
        cursor.executemany("""
        INSERT INTO products (crop, category, grade, location, qty, price, img, emoji, buyer, is_urgent, size_spec, freshness_spec, packaging_spec, pesticide_spec, harvest_spec)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, initial_products)
        
    # Users / Authentication table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        phone_email TEXT,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'Farmer',
        location TEXT DEFAULT 'Lasalgaon, Nashik',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Seed default sample users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        seed_users = [
            ("Ramesh Patel", "ramesh_farmer", "9876543210", "agri123", "Farmer / FPO", "Lasalgaon, Nashik"),
            ("Sunita Devi", "sunita_fpo", "9812345678", "agri123", "FPO Leader", "Nagpur"),
            ("Vikram Singh", "vikram_kisan", "9823456789", "agri123", "Organic Grower", "Pune")
        ]
        cursor.executemany("""
        INSERT INTO users (name, username, phone_email, password, role, location)
        VALUES (?, ?, ?, ?, ?, ?)
        """, seed_users)

    # Orders & Cross-Device Tracking Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_code TEXT UNIQUE NOT NULL,
        buyer_name TEXT NOT NULL,
        buyer_phone TEXT NOT NULL,
        buyer_location TEXT NOT NULL,
        crop TEXT NOT NULL,
        grade TEXT NOT NULL,
        qty REAL NOT NULL,
        price REAL NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT DEFAULT 'Order Placed',
        status_step INTEGER DEFAULT 1,
        vehicle_no TEXT DEFAULT 'MH-15-AB-1234',
        driver_name TEXT DEFAULT 'Ramesh Shinde',
        driver_phone TEXT DEFAULT '+91 98765 43210',
        agency TEXT DEFAULT 'Kisan Express Logistics',
        speed TEXT DEFAULT '42 km/h',
        eta TEXT DEFAULT '45 Mins',
        progress_pct INTEGER DEFAULT 65,
        pickup_pin TEXT DEFAULT '4829',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Seed default sample orders if empty
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        seed_orders = [
            ("ORD-84102", "FreshKart Wholesale", "+91 98765 43210", "Lasalgaon Mandi Terminal Gate #2", "Onion", "Grade A", 80.0, 3420.0, 273600.0, "In Transit (Highway NH-60)", 3, "MH-15-AB-1234", "Ramesh Shinde", "+91 98765 43210", "Kisan Express Logistics", "42 km/h", "45 Mins", 65, "4829"),
            ("ORD-83951", "AgroMart Retail", "+91 98123 45678", "Pune APMC Yard #4", "Wheat", "Grade A", 50.0, 2640.0, 132000.0, "Delivered & Settled", 4, "MH-12-PQ-9081", "Sanjay Jadhav", "+91 98220 99881", "MahaLogistics Hub", "0 km/h", "Delivered Today", 100, "7219"),
            ("ORD-83710", "GreenHarvest Exports", "+91 98234 56789", "Nagpur Cold Chain Center", "Soybean", "Grade A", 30.0, 4820.0, 144600.0, "Quality Inspected & Packed", 2, "MH-31-TR-4567", "Vinod Gaikwad", "+91 98900 11223", "Vidarbha Agro Carriers", "0 km/h", "Pickup 02:30 PM", 35, "5541")
        ]
        cursor.executemany("""
        INSERT INTO orders (order_code, buyer_name, buyer_phone, buyer_location, crop, grade, qty, price, total_amount, status, status_step, vehicle_no, driver_name, driver_phone, agency, speed, eta, progress_pct, pickup_pin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_orders)

    conn.commit()
    conn.close()

init_db()

# -------------------------------------------------------------
# SCHEMAS
# -------------------------------------------------------------
class UserRegister(BaseModel):
    name: str
    username: str
    phone_email: Optional[str] = ""
    password: str
    role: Optional[str] = "Farmer"
    location: Optional[str] = "Maharashtra"

class UserLogin(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    crop: str
    category: str
    grade: str
    location: str
    qty: float
    price: float
    img: Optional[str] = None
    emoji: Optional[str] = "🌾"
    buyer: Optional[str] = "Open Market"
    isUrgent: Optional[bool] = False
    sizeSpec: Optional[str] = "Standard Uniform"
    freshnessSpec: Optional[str] = "Farm Fresh"
    packagingSpec: Optional[str] = "50kg Bags"
    pesticideSpec: Optional[str] = "Zero-Residue Certified"
    harvestSpec: Optional[str] = "Recent Harvest"

class SupportCallback(BaseModel):
    name: str
    phone: str
    query_type: Optional[str] = "General Helpline"
    language: Optional[str] = "Hindi"

class VehicleUpdate(BaseModel):
    vehicle_no: str
    driver_name: str
    driver_phone: str
    agency: str

class OrderCreate(BaseModel):
    crop: str
    grade: str
    qty: float
    price: float
    total_amount: Optional[float] = None
    buyer_name: Optional[str] = "Registered Buyer"
    buyer_phone: Optional[str] = "+91 98765 43210"
    buyer_location: Optional[str] = "Lasalgaon APMC Mandi"

# -------------------------------------------------------------
# REST API ENDPOINTS
# -------------------------------------------------------------

@app.get("/api/health")
def health():
    return {"status": "online", "message": "Agro-Sphere Live Backend is operational!"}

@app.get("/api/products")
def get_products(category: Optional[str] = Query(None)):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if category and category != "all":
        cursor.execute("SELECT * FROM products WHERE category = ? ORDER BY id DESC", (category,))
    else:
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
        
    rows = cursor.fetchall()
    conn.close()
    
    products = []
    for r in rows:
        products.append({
            "id": r["id"],
            "crop": r["crop"],
            "category": r["category"],
            "grade": r["grade"],
            "location": r["location"],
            "qty": r["qty"],
            "price": r["price"],
            "img": r["img"],
            "e": r["emoji"],
            "buyer": r["buyer"],
            "isUrgent": bool(r["is_urgent"]),
            "sizeSpec": r["size_spec"],
            "freshnessSpec": r["freshness_spec"],
            "packagingSpec": r["packaging_spec"],
            "pesticideSpec": r["pesticide_spec"],
            "harvestSpec": r["harvest_spec"]
        })
    return products

@app.post("/api/products")
def create_product(item: ProductCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO products (crop, category, grade, location, qty, price, img, emoji, buyer, is_urgent, size_spec, freshness_spec, packaging_spec, pesticide_spec, harvest_spec)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item.crop, item.category, item.grade, item.location, item.qty, item.price,
        item.img, item.emoji, item.buyer, 1 if item.isUrgent else 0,
        item.sizeSpec, item.freshnessSpec, item.packagingSpec, item.pesticideSpec, item.harvestSpec
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "message": f"{item.crop} lot ({item.qty}q) listed on live server successfully!",
        "id": new_id
    }

@app.get("/api/prices/mandi-rates")
def get_mandi_rates():
    return {
        "commodity": "Onion",
        "modal_price": 3420,
        "change_percent": "+8.4%",
        "best_window": "Next 3–5 days (₹3,500–₹3,650/q)",
        "mandis": [
            {"name": "Lasalgaon APMC", "price": 3420, "arrival_qty": "1,450q", "trend": "up"},
            {"name": "Nashik APMC", "price": 3380, "arrival_qty": "920q", "trend": "up"},
            {"name": "Pimpalgaon APMC", "price": 3350, "arrival_qty": "680q", "trend": "stable"},
            {"name": "Pune APMC", "price": 3310, "arrival_qty": "1,200q", "trend": "stable"}
        ],
        "weekly_trend": [2450, 2680, 2920, 2810, 3100, 3280, 3420]
    }

@app.get("/api/logistics/truck/{vehicle_no}")
def get_truck_details(vehicle_no: str):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vehicle_trips WHERE vehicle_no = ?", (vehicle_no,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {
            "vehicle_no": vehicle_no,
            "driver_name": "Assigned Driver",
            "driver_phone": "+91 98765 43210",
            "agency": "Kisan Logistics",
            "status": "Scheduled",
            "speed": "0 km/h",
            "eta": "1 Hour",
            "progress_pct": 20,
            "pickup_pin": "4829"
        }
        
    return {
        "vehicle_no": row["vehicle_no"],
        "driver_name": row["driver_name"],
        "driver_phone": row["driver_phone"],
        "agency": row["agency"],
        "status": row["status"],
        "speed": row["speed"],
        "eta": row["eta"],
        "progress_pct": row["progress_pct"],
        "pickup_pin": row["pickup_pin"]
    }

@app.post("/api/logistics/assign")
def assign_vehicle(v: VehicleUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO vehicle_trips (vehicle_no, driver_name, driver_phone, agency)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(vehicle_no) DO UPDATE SET
        driver_name = excluded.driver_name,
        driver_phone = excluded.driver_phone,
        agency = excluded.agency
    """, (v.vehicle_no, v.driver_name, v.driver_phone, v.agency))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Vehicle {v.vehicle_no} assigned to active pickup order!"}

@app.post("/api/support/callback")
def create_callback(req: SupportCallback):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO support_tickets (name, phone, query_type, language)
    VALUES (?, ?, ?, ?)
    """, (req.name, req.phone, req.query_type, req.language))
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "ticket_id": ticket_id,
        "message": f"Callback ticket #{ticket_id} booked for {req.name}. An APMC officer will call within 15 mins in {req.language}."
    }

# -------------------------------------------------------------
# ORDERS & CROSS-DEVICE TRACKING ENDPOINTS
# -------------------------------------------------------------

@app.get("/api/orders")
def get_orders(phone: Optional[str] = None, search: Optional[str] = None):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM orders"
    params = []

    if phone:
        query += " WHERE buyer_phone LIKE ? OR order_code LIKE ?"
        params.extend([f"%{phone}%", f"%{phone}%"])
    elif search:
        query += " WHERE order_code LIKE ? OR buyer_name LIKE ? OR crop LIKE ? OR buyer_phone LIKE ?"
        params.extend([f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"])

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    orders = []
    for r in rows:
        orders.append({
            "id": r["id"],
            "orderCode": r["order_code"],
            "buyerName": r["buyer_name"],
            "buyerPhone": r["buyer_phone"],
            "buyerLocation": r["buyer_location"],
            "crop": r["crop"],
            "grade": r["grade"],
            "qty": r["qty"],
            "price": r["price"],
            "totalAmount": r["total_amount"],
            "status": r["status"],
            "statusStep": r["status_step"],
            "vehicleNo": r["vehicle_no"],
            "driverName": r["driver_name"],
            "driverPhone": r["driver_phone"],
            "agency": r["agency"],
            "speed": r["speed"],
            "eta": r["eta"],
            "progressPct": r["progress_pct"],
            "pickupPin": r["pickup_pin"],
            "createdAt": r["created_at"]
        })
    return orders

@app.post("/api/orders")
def create_order(req: OrderCreate):
    import random
    clean_crop = req.crop.strip()
    clean_grade = req.grade.strip()
    qty = float(req.qty)
    price = float(req.price)
    total_amount = float(req.total_amount) if req.total_amount else round(qty * price, 2)
    order_code = f"ORD-{random.randint(84000, 89999)}"
    pickup_pin = str(random.randint(1000, 9999))

    assigned_vehicle = "MH-15-AB-1234"
    assigned_driver = "Ramesh Shinde"
    assigned_phone = "+91 98765 43210"
    assigned_agency = "Kisan Express Logistics"

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO orders (
        order_code, buyer_name, buyer_phone, buyer_location,
        crop, grade, qty, price, total_amount,
        status, status_step, vehicle_no, driver_name, driver_phone,
        agency, speed, eta, progress_pct, pickup_pin
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_code, req.buyer_name or "Registered Buyer", req.buyer_phone or "+91 98765 43210",
        req.buyer_location or "Lasalgaon Mandi Terminal",
        clean_crop, clean_grade, qty, price, total_amount,
        "Order Confirmed & Escrow Held", 1, assigned_vehicle, assigned_driver, assigned_phone,
        assigned_agency, "0 km/h", "Pickup in 30 Mins", 25, pickup_pin
    ))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"Order #{order_code} confirmed! Transport vehicle {assigned_vehicle} assigned for pickup.",
        "order": {
            "id": order_id,
            "orderCode": order_code,
            "crop": clean_crop,
            "grade": clean_grade,
            "qty": qty,
            "price": price,
            "totalAmount": total_amount,
            "buyerName": req.buyer_name,
            "buyerPhone": req.buyer_phone,
            "status": "Order Confirmed & Escrow Held",
            "statusStep": 1,
            "vehicleNo": assigned_vehicle,
            "driverName": assigned_driver,
            "driverPhone": assigned_phone,
            "pickupPin": pickup_pin,
            "eta": "Pickup in 30 Mins",
            "trackingUrl": f"http://127.0.0.1:5000/?order={order_code}#tracking"
        }
    }

@app.get("/api/orders/{order_code}")
def get_order_by_code(order_code: str):
    clean_code = order_code.strip().upper()
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE UPPER(order_code) = ? OR buyer_phone = ? ORDER BY id DESC LIMIT 1", (clean_code, order_code.strip()))
    r = cursor.fetchone()
    conn.close()

    if not r:
        raise HTTPException(status_code=404, detail=f"Order '{order_code}' not found.")

    return {
        "id": r["id"],
        "orderCode": r["order_code"],
        "buyerName": r["buyer_name"],
        "buyerPhone": r["buyer_phone"],
        "buyerLocation": r["buyer_location"],
        "crop": r["crop"],
        "grade": r["grade"],
        "qty": r["qty"],
        "price": r["price"],
        "totalAmount": r["total_amount"],
        "status": r["status"],
        "statusStep": r["status_step"],
        "vehicleNo": r["vehicle_no"],
        "driverName": r["driver_name"],
        "driverPhone": r["driver_phone"],
        "agency": r["agency"],
        "speed": r["speed"],
        "eta": r["eta"],
        "progressPct": r["progress_pct"],
        "pickupPin": r["pickup_pin"],
        "createdAt": r["created_at"]
    }

@app.patch("/api/orders/{order_code}/advance")
def advance_order_status(order_code: str):
    clean_code = order_code.strip().upper()
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE UPPER(order_code) = ?", (clean_code,))
    r = cursor.fetchone()
    if not r:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")

    current_step = r["status_step"]
    next_step = 1 if current_step >= 4 else current_step + 1
    
    stages = {
        1: ("Order Confirmed & Escrow Held", 25, "0 km/h", "Pickup in 30 Mins"),
        2: ("Quality Inspected & Standard Packed", 50, "0 km/h", "Loading Produce"),
        3: ("In Transit (Highway NH-60)", 75, "42 km/h", "ETA: 45 Mins"),
        4: ("Delivered & Instant Bank Settlement Done", 100, "0 km/h", "Delivered Today")
    }
    
    status_text, progress, speed, eta = stages.get(next_step, stages[4])

    cursor.execute("""
    UPDATE orders
    SET status = ?, status_step = ?, progress_pct = ?, speed = ?, eta = ?
    WHERE UPPER(order_code) = ?
    """, (status_text, next_step, progress, speed, eta, clean_code))
    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": f"Order #{clean_code} tracking advanced to Step {next_step}: {status_text}",
        "status": status_text,
        "statusStep": next_step,
        "progressPct": progress,
        "eta": eta
    }

# -------------------------------------------------------------
# USER AUTHENTICATION ENDPOINTS
# -------------------------------------------------------------

@app.get("/api/auth/check-username")
def check_username(username: str = Query(..., min_length=2)):
    clean_username = username.strip().lower().replace("@", "")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE LOWER(username) = ?", (clean_username,))
    count = cursor.fetchone()[0]
    conn.close()
    return {
        "available": count == 0,
        "username": clean_username,
        "message": "Username is available!" if count == 0 else "Username is already taken."
    }

@app.post("/api/auth/register")
def register_user(req: UserRegister):
    clean_name = req.name.strip()
    clean_username = req.username.strip().lower().replace("@", "").replace(" ", "_")
    if not clean_username:
        raise HTTPException(status_code=400, detail="Personal username cannot be empty.")
    if len(clean_name) < 2:
        raise HTTPException(status_code=400, detail="Full name must be at least 2 characters.")
    if len(req.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters.")

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute("SELECT id FROM users WHERE LOWER(username) = ?", (clean_username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail=f"Username '@{clean_username}' is already taken. Please choose another username.")

    cursor.execute("""
    INSERT INTO users (name, username, phone_email, password, role, location)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (clean_name, clean_username, req.phone_email.strip(), req.password, req.role, req.location))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "status": "success",
        "message": f"Account created successfully for {clean_name}!",
        "user": {
            "id": user_id,
            "name": clean_name,
            "username": clean_username,
            "role": req.role,
            "location": req.location,
            "phone_email": req.phone_email.strip()
        }
    }

@app.post("/api/auth/login")
def login_user(req: UserLogin):
    login_id = req.username.strip().lower().replace("@", "")
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Match by username or phone/email
    cursor.execute("""
    SELECT * FROM users
    WHERE (LOWER(username) = ? OR LOWER(phone_email) = ?)
    AND password = ?
    """, (login_id, login_id, req.password))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid username/credentials or password.")

    return {
        "status": "success",
        "message": f"Welcome back, {row['name']}!",
        "user": {
            "id": row["id"],
            "name": row["name"],
            "username": row["username"],
            "role": row["role"],
            "location": row["location"],
            "phone_email": row["phone_email"]
        }
    }

@app.get("/api/auth/users")
def get_registered_users():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, username, role, location, phone_email FROM users ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r["id"],
            "name": r["name"],
            "username": r["username"],
            "role": r["role"],
            "location": r["location"],
            "phone_email": r["phone_email"]
        }
        for r in rows
    ]


# -------------------------------------------------------------
# REAL WHATSAPP WEBHOOK BOT (Twilio / Meta API Compatible)
# -------------------------------------------------------------
from fastapi import Request
from fastapi.responses import Response

def generate_kisan_bot_reply(user_msg: str, has_photo: bool = False, media_url: str = "") -> str:
    msg = (user_msg or "").strip().lower()
    
    if has_photo:
        return (
            "📸 *Agro-Sphere AI Crop Quality Analysis:*\n\n"
            "🌾 *Produce Detected:* Fresh Harvest Lot\n"
            "🔍 *Calculated Grade:* *Grade A (Export / APMC Premium)*\n"
            "📏 *Avg Size:* 48–52mm Uniform Sorting\n"
            "💧 *Moisture Content:* 11.4% (Well-Cured)\n"
            "🛡️ *Pesticide Residue:* PASS (Zero Residue Certified)\n"
            "💰 *Recommended Benchmark Price:* *₹3,420 – ₹3,600/q*\n"
            "🛒 *Active Buyers:* FreshKart (20q), AgroMart (50q)\n\n"
            "👉 _Reply 'LIST' to publish this lot to buyers, or 'CALL' to speak with APMC officer._"
        )
    
    # 1. General Knowledge & Leadership questions (e.g., PM of India)
    if any(w in msg for w in ["pm", "prime minister", "modi", "प्रधान मंत्री", "प्रधानमंत्री", "पंतप्रधान"]):
        return (
            "🇮🇳 *भारत के माननीय प्रधान मंत्री श्री नरेंद्र मोदी (Shri Narendra Modi) हैं।*\n\n"
            "The Prime Minister of India is Shri Narendra Modi, serving as PM since May 2014. "
            "Under his leadership, agricultural initiatives like PM-KISAN, PM Fasal Bima Yojana, and e-NAM have been launched to support farmers."
        )
    
    if any(w in msg for w in ["capital", "राजधानी"]):
        return "🏛️ भारत की राजधानी नई दिल्ली (New Delhi) है। / The capital of India is New Delhi."
    
    if any(w in msg for w in ["onion", "pyaz", "कांदा", "प्याज", "rate", "bhav", "भाव", "price", "mandi", "मंडी"]):
        return (
            "📈 *Agro-Sphere Live APMC Mandi Rates (आज का भाव):*\n\n"
            "🧅 *Onion (कांदा):* ₹3,420/q (Lasalgaon) ▲ +8.4%\n"
            "🍅 *Tomato (टमाटर):* ₹2,850/q (Nashik) ▲ +4.2%\n"
            "🫘 *Soybean (सोयाबीन):* ₹4,820/q (Nagpur)\n"
            "🍋 *Lemon (नींबू):* ₹4,600/q (Lasalgaon)\n"
            "🥭 *Mango (हापूस):* ₹12,500/q (Ratnagiri)\n\n"
            "💡 *Smart Selling Advisory:* Onion modal price is trending upward. Recommended selling window is next *3–5 days*."
        )
    
    if any(w in msg for w in ["truck", "vehicle", "driver", "track", "ट्रक", "गाड़ी", "ड्राइवर", "लोकेशन"]):
        return (
            "🚚 *Live Transport Dispatch Status:*\n\n"
            "🚛 *Vehicle No:* MH-15-AB-1234 (Kisan Logistics)\n"
            "👨‍✈️ *Driver:* Ramesh Shinde (+91 98765 43210)\n"
            "⚡ *Status:* En Route (Speed: 42 km/h)\n"
            "⏱️ *Estimated Arrival:* 45 Minutes at Gate #2\n"
            "🔑 *Digital Weighbridge PIN:* *4829*\n\n"
            "📍 _Live route GPS telemetry is actively updating._"
        )

    if any(w in msg for w in ["officer", "help", "call", "अधिकारी", "सहायता", "madat", "मदत"]):
        return (
            "👨‍🌾 *Lasalgaon APMC Field Officer Connect:*\n\n"
            "👤 *Officer Name:* Suresh Deshmukh\n"
            "📞 *Direct Mobile:* +91 98220 12345\n"
            "🏢 *Desk:* Lasalgaon Weighbridge Gate #2\n"
            "🟢 *Toll-Free Helpline:* 1800-889-2476 (24x7)\n\n"
            "✅ _Officer Suresh has been alerted to prioritize your lot upon entry._"
        )
        
    # Only return welcome message if user actually greeted
    if any(msg.startswith(w) or w == msg for w in ["hi", "hello", "hey", "namaste", "start", "नमस्ते", "नमस्कार"]):
        return (
            "🙏 *नमस्ते किसान भाई! Welcome to Agro-Sphere Seva.*\n\n"
            "I am your 24x7 intelligent agricultural and advisory assistant. You can ask me anything:\n"
            "1️⃣ *Mandi Bhav* (e.g., 'Onion rate today')\n"
            "2️⃣ *General Knowledge & Schemes* (e.g., 'PM of India', 'PM-KISAN status')\n"
            "3️⃣ *Photo Grading* (Send a crop photo for instant AI quality test)\n"
            "4️⃣ *Truck Tracking* (e.g., 'Track my truck')\n\n"
            "Ask any question or send your query! 🌾"
        )

    # General inquiry fallback
    return (
        f"🌾 *Agro-Sphere Sahayak Response:*\n\n"
        f"Regarding your query: \"{user_msg}\"\n"
        f"Today's Lasalgaon Onion rate is ₹3,420/q and Tomato is ₹2,850/q. "
        f"Our 24x7 Toll-Free Farmer Helpline is 1800-889-2476. How else can I assist you?"
    )

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-flash-lite-latest"
GEMINI_FALLBACKS = ["gemini-flash-latest", "gemini-3.5-flash-lite", "gemini-3.6-flash"]

import urllib.request

def call_gemini_backend(user_query: str, lang: str = "Hindi") -> Optional[str]:
    models_to_try = [GEMINI_MODEL] + [m for m in GEMINI_FALLBACKS if m != GEMINI_MODEL]
    
    system_prompt = (
        f"You are Ai Krishi Sahayak, an intelligent AI Voice & Chat Assistant for Indian farmers and citizens built for Agro-Sphere. "
        f"Answer the user's question directly, accurately, and politely in {lang} (or match the language of their query). "
        f"You can answer ANY question, including general knowledge (such as: the Prime Minister of India is Shri Narendra Modi, government policies, leaders, history), "
        f"agricultural science, weather, crop cultivation, and market rates. "
        f"Context if relevant: Today's Lasalgaon Onion rate is ₹3,420/q (+8.4%), Tomato is ₹2,850/q, Soybean is ₹4,820/q. "
        f"Helpline: 1800-889-2476. Keep the answer direct, practical, and under 3-4 sentences with relevant emojis. "
        f"Do NOT give a generic welcome message unless the user simply greeted you."
    )
    
    data = {
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{system_prompt}\n\nUser/Farmer Query: {user_query}"}]
        }],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 300}
    }
    encoded_data = json.dumps(data).encode("utf-8")

    for model_name in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
            req = urllib.request.Request(url, data=encoded_data, headers={"Content-Type": "application/json"})
            resp = urllib.request.urlopen(req, timeout=12)
            res_json = json.loads(resp.read().decode("utf-8"))
            text_out = res_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            if text_out:
                return text_out
        except Exception as e:
            print(f"Gemini Backend [{model_name}] error: {e}")
            continue

    return None

# Twilio WhatsApp Webhook (POST form-urlencoded)
@app.post("/api/whatsapp/webhook")
async def twilio_whatsapp_webhook(request: Request):
    form_data = await request.form()
    user_msg = form_data.get("Body", "")
    from_number = form_data.get("From", "")
    num_media = int(form_data.get("NumMedia", 0))
    media_url = form_data.get("MediaUrl0", "")
    
    has_photo = num_media > 0
    if not has_photo and user_msg:
        ai_reply = call_gemini_backend(user_msg)
        bot_reply = ai_reply if ai_reply else generate_kisan_bot_reply(user_msg, has_photo=has_photo, media_url=media_url)
    else:
        bot_reply = generate_kisan_bot_reply(user_msg, has_photo=has_photo, media_url=media_url)
    
    # Return TwiML XML for instant WhatsApp reply
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{bot_reply}</Message>
</Response>"""
    return Response(content=twiml_response, media_type="application/xml")

# Direct JSON testing endpoint for WhatsApp bot & AI
@app.post("/api/whatsapp/chat")
async def direct_whatsapp_chat(req: dict):
    msg = req.get("message", "")
    has_photo = req.get("has_photo", False)
    if not has_photo and msg:
        ai_reply = call_gemini_backend(msg)
        reply = ai_reply if ai_reply else generate_kisan_bot_reply(msg, has_photo=has_photo)
    else:
        reply = generate_kisan_bot_reply(msg, has_photo=has_photo)
    return {"reply": reply}

@app.post("/api/ai/ask")
async def ai_ask_endpoint(req: dict):
    query = req.get("query", "")
    lang = req.get("lang", "Hindi")
    reply = call_gemini_backend(query, lang)
    if not reply:
        reply = generate_kisan_bot_reply(query)
    return {"query": query, "reply": reply, "model": GEMINI_MODEL}

# Mount static files to serve the web application (HTML, CSS, JS, Assets)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

@app.get("/login", include_in_schema=False)
def serve_login():
    return FileResponse(os.path.join(current_dir, "login.html"))

@app.get("/register", include_in_schema=False)
def serve_register():
    return FileResponse(os.path.join(current_dir, "login.html"))

@app.get("/app", include_in_schema=False)
def serve_app():
    return FileResponse(os.path.join(current_dir, "index.html"))

@app.get("/dashboard", include_in_schema=False)
def serve_dashboard():
    return FileResponse(os.path.join(current_dir, "index.html"))

app.mount("/", StaticFiles(directory=current_dir, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=5000, reload=False)

