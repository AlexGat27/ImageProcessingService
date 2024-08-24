from enum import Enum

class AppNames(Enum):
    UNITY = "Unity"
    GEOSYSTEM = "Geosystem"
    ADMIN = "Admin"

class AppPorts(Enum):
    UNITY = 6002
    GEOSYSTEM = 6001
    ADMIN = 6000