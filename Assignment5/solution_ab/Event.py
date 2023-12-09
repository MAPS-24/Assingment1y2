from enum import Enum, auto


class EventType(Enum):
    TIMER_INTERRUPT = auto()
    FROM_LAYER5 = auto()
    FROM_LAYER3 = auto()


class Event:
    def __init__(self, ev_time, ev_type, ev_entity, packet=None):
        self.ev_time = ev_time
        self.ev_type = ev_type
        self.ev_entity = ev_entity
        self.packet = packet
