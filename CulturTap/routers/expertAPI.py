from .. import *
from ..classes.database import database
from ..models.expert_card import expertCard
from ..admin.credentials import DB_URL, DB_HEADERS, TOKEN

router = APIRouter(prefix='/user/expertCard', tags=['Expert Cards'])

# --USER DATA

client = database.expertCard(url=DB_URL, header=DB_HEADERS)


@router.get("/get/{uid}", status_code=status.HTTP_200_OK, response_model=expertCard)
def get_data_by_uid(uid: int, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.show(uid=uid)[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=list[expertCard])
def get_data_by_matching(params: dict, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.show(**params)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
