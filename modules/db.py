# modules/db.py
import pymongo
from datetime import datetime

# Configurar la conexión a MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["chat_database"]  # Nombre de la base de datos
conversations_collection = db["conversations"]  # Nombre de la colección

def save_conversation(user_message, bot_response):
    conversation = {
        "timestamp": datetime.utcnow(),
        "user_message": user_message,
        "bot_response": bot_response
    }
    conversations_collection.insert_one(conversation)

def get_all_conversations():
    return list(conversations_collection.find().sort("timestamp", pymongo.ASCENDING))