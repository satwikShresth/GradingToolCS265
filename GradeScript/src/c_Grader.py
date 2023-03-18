import os
from enum import Enum


class permission(Enum):
    GRANTED = 1
    REQUESTED = 0
    DENIED = -1


class c_Grader:
    def __init__(self, username, name, hashKey):
        self.username: str = username
        self.name: str = name
        self.hashKey = hashKey
        self.home_directory = os.path.expanduser(f"~{self.username}")
        self.status: permission = permission.REQUESTED
