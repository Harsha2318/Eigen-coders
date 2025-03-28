from pymongo import MongoClient
import redis

# Test MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["EigenCoders"]
print("✅ MongoDB Connected:", db.list_collection_names())

# Test Redis
redis_client = redis.Redis(host='localhost', port=6379)
redis_client.set("test", "Redis is working!")
print("✅ Redis Test:", redis_client.get("test").decode())
