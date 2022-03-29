from bson import ObjectId
from pymongo import MongoClient

# conn = MongoClient("mongodb+srv://bubot:babcockbot@bubotcluster.mp3tz.mongodb.net/chatbot?retryWrites=true&w=majority",  serverSelectionTimeoutMS=5000)
MONGODB_URL = "mongodb+srv://bubot:babcockbot@bubotcluster.mp3tz.mongodb.net/chatbot?retryWrites=true&w=majority"
# "mongodb+srv://bubot:babcockbot@bubotcluster.mp3tz.mongodb.net/chatbot"
DATABASE_NAME = "chatbot"

try:
    class Database():
        
        def __init__(self) -> None:
            self.connected = False
            self.mongodb_client = None 

        async def db_connection(self):
            if self.connected == False:
                self.client = MongoClient(MONGODB_URL)
                # AsyncIOMotorClient("mongodb+srv://bubot:babcockbot@bubotcluster.mp3tz.mongodb.net/chatbot?retryWrites=true&w=majority")
                self.connected = True

            db = self.client[DATABASE_NAME]
            print(db.list_collection_names())
            
           
            return db
    

    class PyObjectId(ObjectId):
        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def validate(cls, v):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid objectid")
            return ObjectId(v)

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(type="string")

except Exception as e:
    print("Unable to connect to the server.")
    print('error:', e)


def ResponseModel(data, code, message, error):
    return {
        "data": [data],
        "code": code,
        "message": message,
        "error": error
    }