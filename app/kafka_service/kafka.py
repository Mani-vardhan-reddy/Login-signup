import uuid
import json
import asyncio
from confluent_kafka import Producer, Consumer
from app.core.config import settings

class KafkaService():
    
    def __init__(self):
        self.producer_conf = {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "retries": settings.KAFKA_RETRIES,
            "enable.idempotence": True,
        }
        
    async def delivery_report(self, err, msg):
        if err:
            print(f"Delivery Failed for {msg.key()}: {err}")
        else:
            print(f"Message Delivered to {msg.topic()} [{msg.partition()}] offset {msg.offset()}")
    
    async def get_producer(self):
        return Producer(self.producer_conf)
    
    async def produce_message(self, topic: str, value: dict):
        producer = await self.get_producer()
        key= str(uuid.uuid4())
        producer.produce(
            topic= topic,
            key= key.encode('utf-8'),
            value= json.dumps(value).encode('utf-8'),
            callback= lambda err, msg : asyncio.create_task(self.delivery_report(err, msg))
        )
        
        producer.flush()
    
kafka_service = KafkaService()