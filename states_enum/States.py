from enum import Enum


class States_TCU(Enum):
    OFF = "OFF"
    HEATING = "HEATING" 
    READY = "READY"


class States_SCU(Enum):
    OFF = "OFF"
    WAITING = "WAITING"
    VALID_REQUEST = "VALID_REQUEST"