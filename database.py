from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "CRUD_Animals")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

print(f"Connected to database: {DB_NAME}")

def get_db():
    return db