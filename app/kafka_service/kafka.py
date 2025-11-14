import json
from confluent_kafka import Producer, Consumer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from typing import List
from app.core.config import settings

class KafkaService():
    def __init__(self, broker_url):
        self.broker_url = broker_url
        self._producer = None
        self._consumer = {}
        
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
        if not self._consumer:
            try:
                self._consumer = Consumer(
                    {
                        "bootstrap.servers": self.broker_url
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
                key = key.encode('utf-8'),
                value = json.dumps(value),
                callback = self.delivery_report
            )
            producer.flush()
            
        except KafkaException as e:
            raise
        
    @staticmethod
    def delivery_report(errmsg, msg):
        if errmsg is not None:
            print(f"Message Failed to produce to the topic {msg.topic()} : {errmsg}")
            return
        print(f"Message Successfully produced to Toipc {msg.topic()}, partition {msg.partition()} and offset {msg.offset()}")
    
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