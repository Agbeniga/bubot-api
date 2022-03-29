from fastapi import APIRouter, WebSocket
from fastapi.security import OAuth2PasswordBearer
from ml import algorithmn
from config.db import Database


main_route = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# Index route

@main_route.get('/')
def index():
    return {'message': "Hello, from BUBot"}

@main_route.get('/Welcome')
def get_name(name: str):
    return {'Welcome from BUBot': f'{name}'}

@main_route.post('/chat')
def get_name(name: str):
    print(name)
    bot = algorithmn.ChatBot()
    
    return {'Welcome from BUBot': f'{bot.botResponse(name)}'}

# @main_route
# async def auth(token: str = Depends(oauth2_scheme)):
#     return {"token":token}

manager: algorithmn.ConnectionManager = algorithmn.ConnectionManager()
bot = algorithmn.ChatBot()
database = Database()


@main_route.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    db = await database.db_connection()
    await manager.connect(websocket)
    data = await websocket.receive_json()
    print("stop it")
    print(data["question"])
    bot_response = bot.botResponse(data["question"])
    await manager.reply(bot_response, websocket)
    db.message.insert_one({"question": data["question"], "answer":bot_response, "device_id":data["device_id"]})
        
        
    while True:
        try:
            data = await websocket.receive_json()
            bot_response = bot.botResponse(data["question"])
            await manager.reply(bot_response, websocket)
            db.message.insert_one({"question": data["question"], "answer":bot_response, "device_id":data["device_id"]})
            pass
        except Exception as e:
            print('error:', e)
            manager.disconnect(websocket)
            break
    print('Bye..')

@main_route.websocket("/ws/audit")
async def websocket_endpoint(websocket: WebSocket):
    db = await database.db_connection()
    await manager.connect(websocket)
    data = await websocket.receive_text()
    db.audditlog.insert_one({"log":data})
        
    while True:
        try:
            data = await websocket.receive_text()
            db.message.insert_one({"log":data})
        except Exception as e:
            print('error:', e)
            manager.disconnect(websocket)
            break
    print('Bye..')

@main_route.websocket("/ws/log-audit")
async def websocket_endpoint(websocket: WebSocket):
    db = await database.db_connection()
    await manager.connect(websocket)
    logs = db.audditlog.find()
    await manager.reply(logs, websocket)
    
        
    while True:
        try:
            logs = db.audditlog.find()
            await manager.reply(logs, websocket)
        except Exception as e:
            print('error:', e)
            manager.disconnect(websocket)
            break
    print('Bye..')