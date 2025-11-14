import uuid
from app.kafka_service.kafka import kafka_service

class NotificationService():
    
    def __init__(self, connector):
        self.connector = connector
        
    def send_notification(self, payload, topic):
        try:
            self.connector.produce_message(
                topic= topic,
                key= str(uuid.uuid4()),
                value= payload
            )
            print(f"Notification sent → topic={topic}")
        except Exception as e:
            print(f"Failed to send notification: {e}")
            raise e
        
notification_service = NotificationService(connector=kafka_service)