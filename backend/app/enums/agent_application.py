from enum import Enum


class GumbaApplicationType(str, Enum):
    EXISTING = "EXISTING"
    NEW = "NEW"