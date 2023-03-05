from .. import *


class Service(BaseModel):
    uid: int
    availableTime: list[str]
    bandwidth: str
