from .. import *
from ..classes.database import database
from ..models.service import Service
from ..admin.credentials import DB_URL, DB_HEADERS, TOKEN

router = APIRouter(prefix='/user/tripPlanner', tags=['Trip Planner'])

# --USER DATA

client = database.tripPlanner(url=DB_URL, header=DB_HEADERS)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=list[Service])
def get_data(token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.show()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
