from fastapi import APIRouter, HTTPException, Depends,status
from models.user import User, Hash
from config.db import Database
from schemas.user import userEntity, usersEntity
from bson import ObjectId
from pyfcm import FCMNotification
from models.oauth import get_current_user
from models.jwttoken import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


user = APIRouter()

database = Database()
# db = await database.db_connection()
# print(database)

@user.get('/user')
async def find_all_users():
    db = await database.db_connection()
    return usersEntity(db.user.find())

@user.get('/user/{id}')
async def find_user_by_id(id: str):
    db = await database.db_connection()
    data = db.user.find({'_id': str(ObjectId(id))})
    
    return data

@user.post('/user/')
async def create_user(user: User):
    db = await database.db_connection()
    data = db.user.insert_one(dict(user))

    return {"id":str(data.inserted_id)}
    # userEntity(db.user.insert_one(dict(user)))

@user.delete('/user/{id}')
async def delete_user(id, user: User):
    db = await database.db_connection()
    return userEntity(db.user.find_one_and_delete({"_id":ObjectId(id)}))

@user.put('/user/{id}')
async def update_user(id, user: dict):
    db = await database.db_connection()
    db.user.replace_one({"_id":ObjectId(id)},
        user
    )
    return userEntity(db.user.find_one({"_id":ObjectId(id)}))

@user.post('/register')
async def create_user(request:User):
    db = await database.db_connection()
    hashed_pass = Hash.bcrypt(request.password)
    user_object = dict(request)
    user_object["password"] = hashed_pass
    user_id = db.user.insert(user_object)
    return {"res":"created"}


@user.post('/login')
async def login(request:OAuth2PasswordRequestForm = Depends()):
    db = await database.db_connection()
    user = db["users"].find_one({"username":request.username})
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    access_token = create_access_token(data={"sub": user["username"] })
    return {"access_token": access_token, "token_type": "bearer"}



@user.post('/notify-user/')
async def notify_user(question: str, answer:str, device_id:str):
    push_service = FCMNotification(api_key="AAAA7RG6uOs:APA91bEfaJyeVJn5cCPM-bpp3GOWAQoaP2mwVRz-RnXLxuKra5w6Z7fpye_ZwpcfoGFp_wOJIjo0KbIcVEWbjBY7nc15roWWJz5jrcJorhSPY9j6LSUAmTGJCD9rAvLLcV2MjHDJke7G")
 
 
 
    registration_id = device_id
    message_title = f"Question: {question}"
    message_body = f"Answer: {answer}"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
 
    print(result)
    db = await database.db_connection()
    data = db.user.insert_one(dict(user))

    return result