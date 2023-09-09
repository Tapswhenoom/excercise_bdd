class EventSystem:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def publish_event(self, event, publisher = None):
        for subscriber in self.subscribers:
            subscriber.event_handler(event, publisher)