from pydantic import BaseModel

class Chat(BaseModel):
    utterance: str
    bot: str
    phoneId: str