from fastapi import Depends, FastAPI
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
from app.models.item import Item
from app.schema.item import ItemIn

app = FastAPI()


@app.get("/")
async def testing_route():
    return {"Hello": "World"}


@app.get("/health")
async def health_check():
    return {"message": "Api health check successful"}


@app.get("/test")
async def test_route():
    return {"message": "Test route successful"}


@app.get("/health/db")
async def health_db(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"database": "ok"}


@app.post("/items", status_code=201)
async def create_item(item: ItemIn, db: AsyncSession = Depends(get_db)):
    obj = Item(name=item.name)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return {"id": obj.id, "name": obj.name}


@app.get("/items")
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(Item).order_by(Item.id))
    rows = result.all()
    return [{"id": r.id, "name": r.name} for r in rows]
