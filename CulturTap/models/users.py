from .. import *


class userModel(BaseModel):
    uid: int = None
    name: str
    countryCode: str
    phoneNo: int
    profilePic: str = None
    coverPic: list[str] = None
    gender: str = None
    languageSpeak: str = None
    address: str = None
    quote: constr(max_length=100) = None
    followers: int = 0
    followings: int = 0
    profession: str = None
    dob: str = None
    btp: bool = False
    bta: bool = False
    blg: bool = False
    reviews: list[list[int, str]] = None
    pendingRequests: int = 0
    totalRequests: int = 0
    lat: float = None
    long: float = None
    locationFollow: list[str] = None
    availableTime: list[str] = None  # ["6:00:00 am/pm","9:00:00 am/pm"]
    bandwidth: str = 'daily'
