from .. import *


class videoModel_View(BaseModel):
    uid: int
    videoId: int
    url: list[str]
    address: str
    lat: float
    long: float
    category: str
    genre: str
    title: str
    description: str
    pros: str
    cons: str
    rating: float
    shared: bool
    draft: bool
    views: int
    likes: int


class videoModel_Post(BaseModel):
    uid: int
    url:list[str]=['string']
    address: str
    lat: float
    long: float
    category: str
    genre: str
    title: str
    description: str
    pros: str
    cons: str
    rating: float = 0
    shared: bool = True
    draft: bool = True
    views: int = 0
    likes: int = 0

class s3Response(BaseModel):
  url: list[str]
  videoKeys: list[str]