from .. import *


class scheduleCall(BaseModel):
    callId: str  # don't change
    requestFrom: int
    fromUser:str
    requestTo: int
    toUser:str
    title: str
    from_: str  # yyyy-mm-dd hh:mm:ssam/pm
    to: str  # yyyy-mm-dd hh:mm:ssam/pm
    status: str = "pending"

class scheduleCallAdd(BaseModel):
    requestFrom: int
    requestTo: int
    title: str
    from_: str  # yyyy-mm-dd hh:mm:ssam/pm
    to: str  # yyyy-mm-dd hh:mm:ssam/pm
    status: str = "pending"

class scheduleCallAddResponse(BaseModel):
    insertedId:str
    status:str

class msgCall(BaseModel):
    msg:str