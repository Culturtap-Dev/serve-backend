from .. import *


class OTPmodel(BaseModel):
    status: str
    code: int


class messageModel(BaseModel):
    countryCode: str
    phoneNo: int
    msg: str
