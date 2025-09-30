from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import engine, Base
from app.models import Product, Customer, Order, RepairRequest, Settings  # removed Payment since not in schema?
from app.routes import (
    products_router, customers_router, orders_router, 
    repairs_router, analytics_router, settings_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables are created in Supabase
    Base.metadata.create_all(bind=engine)

    # Insert seed data only if database is empty
    from app.seed import create_seed_data
    create_seed_data()

    yield

app = FastAPI(
    title="E-Commerce API",
    description="A complete FastAPI backend for e-commerce with Supabase + M-Pesa integration",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS (allow frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(products_router)
app.include_router(customers_router)
app.include_router(orders_router)
app.include_router(repairs_router)
app.include_router(analytics_router)
app.include_router(settings_router)

@app.get("/")
async def root():
    return {"message": "E-Commerce API is running with Supabase backend 🎉"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": str(engine.url)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
