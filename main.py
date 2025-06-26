from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud
from schemas import ItemUpdate, ItemCreate, ItemOut

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=ItemOut)
def create(item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, name=item.name, age=item.age, email=item.email)

@app.get("/items/", response_model=list[ItemOut])
def read(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.get("/items/{item_id}", response_model=ItemOut)
def read_one(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item:
        return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.delete("/items/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_item(db, item_id)
    if success:
        return {"message": f"Item {item_id} deleted successfully."}
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.patch("/items/{item_id}", response_model=ItemOut)
def partial_update(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    updated_item = crud.update_item_partial(db, item_id, item_data.dict(exclude_unset=True))
    if updated_item:
        return updated_item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
