from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from typing import Optional


class User(BaseModel):
    #id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    firstName: str= Field(None, title="First Name", max_length=500)
    lastName: str= Field(None, title="Last Name", max_length=500)
    email: EmailStr = Field(None, title="Email")
    password: str
    isSuperAdmin: bool

    def as_dict(self):
        return {
            "id": self.id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
        }


class Login(BaseModel):
    username: str
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    username: Optional[str] = None

pwd_cxt = CryptContext(schemes =["bcrypt"],deprecated="auto")
class Hash():
   def bcrypt(password:str):
      return pwd_cxt.hash(password)
   def verify(hashed,normal):
      return pwd_cxt.verify(normal,hashed)