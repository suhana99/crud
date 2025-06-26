# crud.py
from models import Item
from sqlalchemy.orm import Session

def create_item(db: Session, name: str, age: int = None, email: str = None):
    new_item = Item(name=name, age=age, email=email)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_items(db: Session):
    return db.query(Item).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def delete_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
        return True
    return False

def update_item_partial(db: Session, item_id: int, updates: dict):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None
    for key, value in updates.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item
