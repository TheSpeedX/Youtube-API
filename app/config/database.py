import motor.motor_asyncio
from config.variables import MONGO_CONFIG

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONFIG["HOST"])

db = client[MONGO_CONFIG["DBNAME"]]
