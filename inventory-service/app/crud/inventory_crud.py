from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.inventory_model import InventoryItem

# Add a New Inventory Item to the Database
def add_new_inventory_item(inventory_item_data: InventoryItem, session: Session):
    print("Adding Inventory Item to Database")
    
    session.add(inventory_item_data)
    session.commit()
    session.refresh(inventory_item_data)
    return inventory_item_data

# Get All Inventory Items from the Database
def get_all_inventory_items(session: Session):
    all_inventory_items = session.exec(select(InventoryItem)).all()
    return all_inventory_items

# Get an Inventory Item by ID
def get_inventory_item_by_id(inventory_item_id: int, session: Session):
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory Item not found")
    return inventory_item

# Delete Inventory Item by ID
def delete_inventory_item_by_id(inventory_item_id: int, session: Session):
    # Step 1: Get the Inventory Item by ID
    inventory_item = session.exec(select(InventoryItem).where(InventoryItem.id == inventory_item_id)).one_or_none()
    if inventory_item is None:
        raise HTTPException(status_code=404, detail="Inventory Item not found")
    # Step 2: Delete the Inventory Item
    session.delete(inventory_item)
    session.commit()
    return {"message": "Inventory Item Deleted Successfully"}

# # Update Product by ID
# def update_product_by_id(product_id: int, to_update_product_data:ProductUpdate, session: Session):
#     # Step 1: Get the Product by ID
#     product = session.exec(select(Product).where(Product.id == product_id)).one_or_none()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     # Step 2: Update the Product
#     hero_data = to_update_product_data.model_dump(exclude_unset=True)
#     product.sqlmodel_update(hero_data)
#     session.add(product)
#     session.commit()
#     return product