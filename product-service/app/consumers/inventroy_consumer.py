from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
from app.models.product_model import Product, ProductUpdate
from app.crud.product_crud import validate_product_by_id
from app.deps import get_session



async def consume_inventory_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="inventory-add-stock-consumer-group",
        # auto_offset_reset="earliest",
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print("\n\n RAW INVENTORY MESSAGE\n\n ")
            print(f"Received message on topic {message.topic}")
            print(f"Message Value {message.value}")

            # 1. Extract Poduct Id
            inventory_data = json.loads(message.value.decode())
            product_id = inventory_data["product_id"]
            print("PRODUCT ID", product_id)

            # 2. Check if Product Id is Valid
            with next(get_session()) as session:
                product = validate_product_by_id(product_id=product_id, session=session)
                print("PRODUCT VALIDATION CHECK", product)
                if product is None:
                    print("Product Not Found")
                    
                    continue

            # Here you can add code to process each message.
            # Example: parse the message, store it in a database, etc.
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()
