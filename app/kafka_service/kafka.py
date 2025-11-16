import json
from confluent_kafka import Producer, Consumer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from typing import List
from app.models.signup_models import get_async_db
from app.core.config import settings
from app.common_functions.common_services import common_service

class KafkaService():
    def __init__(self, broker_url):
        self.broker_url = broker_url
        self._producer = None
        self._consumer = None

    def get_producer(self):
        if self._producer is None:
            try:
                self._producer = Producer(
                    {
                        "bootstrap.servers": self.broker_url,
                    }
                )
            except KafkaException as e:
                raise
        return self._producer

    def get_consumer(self):
        if self._consumer is None:
            try:
                self._consumer = Consumer(
                    {
                        "bootstrap.servers": self.broker_url,
                        "group.id": settings.KAFKA_GROUP_ID,
                        "auto.offset.reset": settings.KAFKA_AUTO_OFFSET_RESET,
                    }
                )
            except KafkaException as e:
                raise
        return self._consumer

    def produce_message(self, topic, key, value):
        try:
            producer = self.get_producer()
            producer.produce(
                topic = topic,
                key = key.encode("utf-8"),
                value = json.dumps(value),
                callback = self.delivery_report
            )
            producer.flush()

        except KafkaException as e:
            raise
        
    @staticmethod
    def delivery_report(errmsg, msg):
        if errmsg is not None:
            print(f"Message Failed -> {errmsg}")
            return
        print(
            f"Produced to {msg.topic()} | partition {msg.partition()} | offset {msg.offset()}"
        )

    async def process_message(self, message):
        try:
            data = json.loads(message.value().decode("utf-8"))
            topic = message.topic()

            if topic == "email-topic":
                async for session in get_async_db():
                    await common_service.send_email_notification(data, session)

        except Exception as e:
            raise e

    async def consume_message(self, topic):
        try:
            consumer = self.get_consumer()
            consumer.subscribe([topic])

            while True:
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                await self.process_message(msg)
                consumer.commit(msg)

        except Exception as e:
            raise e
    
    def ensure_topic_exists(self, topics: List[str], num_partitions=1, replication_factor=1):
        admin_client = AdminClient(
            {
                "bootstrap.servers": self.broker_url,
            }
        )
        metadata = admin_client.list_topics(timeout=10)
        missing = [topic for topic in topics if topic not in metadata.topics]
        
        if not missing:
            return
        
        print(f"Creating {len(missing)} Topics")
        
        new_topics = [
            NewTopic(
                topic=t, 
                num_partitions=num_partitions, 
                replication_factor=replication_factor
            )
            for t in missing
        ]
        
        fs = admin_client.create_topics(new_topics, request_timeout= 10)
        
        for topic, f in fs.items():
            try:
                f.result()
                print(f"Successfully created Topic {topic}")
            except KafkaException as e:
                print(f"Failed to create topic {topic}: {e}")
                
    def topic_exist(self, topic: str):
        try:
            admin_client = AdminClient(
                {
                    "bootstrap.servers": self.broker_url,
                }
            )
            metadata = admin_client.list_topics(timeout=10)
            existing = topic in metadata.topics
            return existing
        except Exception as e:
            print(f"Error whilr checking for topic {topic}: {e}")
            return False
        
    def create_topic(self, topic, num_partitions=1, replication_factor=1):
        admin_client = AdminClient(
                {
                    "bootstrap.servers": self.broker_url,
                }
            )
        metadata = admin_client.list_topics(timeout=10)
        if topic in metadata.topics:
            print(f"Topic {topic} already exist")
            return True
        
        new_topic = NewTopic(
            topic=topic, 
            num_partitions=num_partitions, 
            replication_factor=replication_factor
        )
        
        fs = admin_client.create_topics([new_topic], request_timeout=10)
        
        for topic, f in fs.items():
            try:
                f.result()
                print(f"Successfully created Topic {topic}")
            except KafkaException as e:
                print(f"Failed to create topic {topic}: {e}")
                
kafka_service = KafkaService(settings.KAFKA_BROKER_URL)