import uvicorn
from fastapi import FastAPI
# from fastapi.responses import 
from fastapi.middleware.cors import CORSMiddleware
from routes.index import main_route
from routes.user import user



# Create the app object
app = FastAPI()
app.include_router(main_route)
app.include_router(user)

# Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    #allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=4000)
