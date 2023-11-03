import os

DB_URI = os.environ.get(
    "DB_URI", "postgresql://postgres:secret@172.19.0.2:5432/inventory"
)
