from typing import Dict, List, Callable, Any

class EventDispatcher:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def register(self, event_name: str, listener: Callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)
    
    async def dispatch(self, event_name: str, data: Any = None):
        if event_name in self.listeners:
            for listener in self.listeners[event_name]:
                await listener(data)

event_dispatcher = EventDispatcher()