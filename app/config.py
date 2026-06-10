import os
from dataclasses import dataclass

@dataclass
class Config:
    db_host: str = "localhost"
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "stockflow_db"

    def __post_init__(self):
        self.db_host = os.getenv("DB_HOST", self.db_host)
        self.db_user = os.getenv("DB_USER", self.db_user)
        self.db_password = os.getenv("DB_PASSWORD", self.db_password)
        self.db_name = os.getenv("DB_NAME", self.db_name)
