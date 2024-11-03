from Media.config import *
from pyrogram.types import *
from typing import Dict, List, Union
from Media.modules.message import *
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client = AsyncIOMotorClient(MONGO_DB_URL)
db = mongo_client[DB_NAME]

accesdb = db.acces
gcastdb = db['GCAST']
        
#SET_WELCOME
async def set_welcome(text):
    accesdb.users.update_one({"_id": 1}, {"$set": {"welcome": text}}, upsert=True)

async def get_welcome():
    user = await accesdb.users.find_one({"_id": 1})
    if user:
        return user.get("welcome", C15)
    else:
        return C15

#SET_FORCE_SUB
async def set_forcesub(text):
    accesdb.users.update_one({"_id": 1}, {"$set": {"forcesub": text}}, upsert=True)

async def get_forcesub():
    user = await accesdb.users.find_one({"_id": 1})
    if user:
        return user.get("forcesub", C45)
    else:
        return C45

#SET_LOGS
async def set_logs(text):
    accesdb.users.update_one({"_id": 1}, {"$set": {"logger": text}}, upsert=True)

async def get_logs():
    user = await accesdb.users.find_one({"_id": 1})
    if user:
        return user.get("logger", C45)
    else:
        return C45
        
#SET_LINK
async def set_link(text):
    accesdb.users.update_one({"_id": 1}, {"$set": {"link": text}}, upsert=True)

async def get_link():
    user = await accesdb.users.find_one({"_id": 1})
    if user:
        return user.get("link")
    else:
        return None
        
#SET_HARGA
async def set_harga(text):
    accesdb.users.update_one({"_id": 1}, {"$set": {"harga": text}}, upsert=True)

async def get_harga():
    user = await accesdb.users.find_one({"_id": 1})
    if user:
        return user.get("harga", K10)
    else:
        return K10

#SET_ID
async def get_id(user_id):
    user = await accesdb.users.find_one({"_id": user_id})
    if user:
        return user.get("id")
    else:
        return None
        
async def set_id(user_id, text):
    accesdb.users.update_one({"_id": user_id}, {"$set": {"id": text}}, upsert=True)

#SET_PRICE
async def get_price(user_id):
    user = await accesdb.users.find_one({"_id": user_id})
    if user:
        return user.get("price")
    else:
        return None
        
async def set_price(user_id, text):
    accesdb.users.update_one({"_id": user_id}, {"$set": {"price": text}}, upsert=True)
        
#SET_CODE
async def get_code(user_id):
    user = await accesdb.users.find_one({"_id": user_id})
    if user:
        return user.get("code")
    else:
        return None
        
async def set_code(user_id, text):
    accesdb.users.update_one({"_id": user_id}, {"$set": {"code": text}}, upsert=True)
        
#MAINTENANCE
async def get_maintenance():
    result = await accesdb.users.find_one({"_id": 1})
    if result:
        return result.get("maintenance", False)
    else:
        return False
        
async def maintenance_on(message: Message) -> bool:
    try:
        result = await accesdb.users.update_one(
            {"_id": 1},
            {'$set': {'maintenance': True}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            return True
    except:
        return False

async def maintenance_off(message: Message) -> bool:
    try:
        result = await accesdb.users.update_one(
            {"_id": 1},
            {'$set': {'maintenance': False}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            return False
    except:
        return False

async def get_type():
    result = await accesdb.users.find_one({"_id": 1})
    if result:
        return result.get("type", True)
    else:
        return True 
        
async def type_on(message: Message) -> bool:
    try:
        result = await accesdb.users.update_one(
            {"_id": 1},
            {'$set': {'type': True}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            return True
    except:
        return False

async def type_off(message: Message) -> bool:
    try:
        result = await accesdb.users.update_one(
            {"_id": 1},
            {'$set': {'type': False}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            return False
    except:
        return False
        
#BROADCAST_USER
async def get_gcast() -> list:
    gcast = await gcastdb.find_one({"gcast_id": "gcast_id"})
    if not gcast:
        return []
    return gcast["gcast"]

async def add_gcast(user_id: int) -> bool:
    gcast = await get_gcast()
    gcast.append(user_id)
    await gcastdb.update_one(
        {"gcast_id": "gcast_id"}, {"$set": {"gcast": gcast}}, upsert=True
    )
    return True

async def remove_gcast(user_id: int) -> bool:
    gcast = await get_gcast()
    gcast.remove(user_id)
    await gcastdb.update_one(
        {"gcast_id": "gcast_id"}, {"$set": {"gcast": gcast}}, upsert=True
    )
    return True
