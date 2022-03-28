from pydantic import BaseModel

class AuditLog(BaseModel):
    log: str