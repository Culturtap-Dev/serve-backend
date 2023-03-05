from .. import *


class expertCard(BaseModel):
    uid: int
    expertLocation: str = None
    visitedPlace: int = 0
    coveredPlace: int = 0
    rating: float = 0
    status: str = None
