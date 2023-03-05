from .. import *
from ..classes.database import database
from ..classes.S3 import Boto3
from ..models.users import userModel
from ..admin.credentials import DB_URL, DB_HEADERS, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TOKEN
from ..constants import *
from ..utils import *

router = APIRouter(prefix='/user', tags=['Users'])

# --USER DATA

users = database.Users(url=DB_URL, header=DB_HEADERS)
s3 = Boto3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=list[userModel])
def get_all_userData(token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        data = users.show()[1:]
        return data
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/get/{uid}", status_code=status.HTTP_200_OK, response_model=userModel)
def get_data_by_uid(uid: int):
    try:
        return users.show(uid=uid)[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/get/matching", status_code=status.HTTP_200_OK, response_model=list[userModel])
def get_data_by_matching(params: dict, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return users.show(**params)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/get/by-distance/uid={currentUID}", status_code=status.HTTP_200_OK, response_model=list[userModel])
def get_data_by_location(currentUID: int, maxKm: float, filtor: dict, minKm: float = 0):
    try:
        user = []
        currentUser = users.show(uid=currentUID)[0]
        lat1, long1 = round(currentUser['lat'], 2), round(
            currentUser['long'], 2)
        for i in users.show(**filtor):
            lat2, long2 = round(i['lat'], 2), round(i['long'], 2)
            differ=lat_long_difference((lat2, long2), (lat1, long1))
            if minKm <= differ>= maxKm:
                i['distance']=differ
                user.append(i)
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/add', status_code=status.HTTP_201_CREATED)
def adding_user(params: userModel, token: str):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    params = params.dict()
    try:
        if users.matchUserDetail(countryCode=params['countryCode'], phoneNo=params['phoneNo']):
            return {'message': "already existed", 'uid': users.uid}

        data = users.add(**params)
        expert = {"uid": data['uid'], "expertLocation": None,
                  "visitedPlace": 0, "coveredPlace": 0, "rating": 0, "status": 'Low'}
        database.expertCard(DB_URL, DB_HEADERS).add(**expert)
        return data
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/add-photo', status_code=status.HTTP_200_OK)
async def adding_pics(uid: int, action: str = 'add', profilePic: list[UploadFile] = None, coverPic: Union[list[UploadFile], None] = None):
    try:
        toUpdate = {}
        if coverPic:
            userData = get_data_by_uid(uid)
            coverPic_keys = []
            urls = []
            for item in coverPic:
                if item.content_type in FILETYPES:
                    key = f'{uuid4()}.{FILETYPES[item.content_type]}'
                    data = await item.read()
                    s3.upload(file=data, key=key,
                              folder=COVER_PIC, bucket=BUCKET)
                    url = f'https://{BUCKET}.s3.ap-south-1.amazonaws.com/{COVER_PIC}{key}'
                    urls.append(url)
                    coverPic_keys.append(f"{COVER_PIC}{key}")
                else:
                    raise
            if action.lower() == 'add':
                if existingPic := userData.get('coverPic'):
                    urls += existingPic
            else:
                if keys := userData.get('coverPic-keys'):
                    for i in keys:
                        s3.delete(bucket=BUCKET, key=i)
            toUpdate['coverPic'] = urls
            toUpdate['coverPic-keys'] = coverPic_keys

        if profilePic:
            if profilePic[-1].content_type in FILETYPES:
                key = f'{uuid4()}.{FILETYPES[profilePic[-1].content_type]}'
                data = await profilePic[-1].read()
                s3.upload(file=data, key=key,
                          folder=PROFILE_PIC, bucket=BUCKET)
                url = f'https://{BUCKET}.s3.ap-south-1.amazonaws.com/{PROFILE_PIC}{key}'
                toUpdate['profilePic'] = url
                toUpdate['profilePic-key'] = f"{PROFILE_PIC}{key}"
                if key := get_data_by_uid(uid).get('profilePic-key'):
                    s3.delete(bucket=BUCKET, key=key)
            else:
                raise
        update_data(uid, toUpdate)
        return toUpdate
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.patch('/update/{uid}', status_code=status.HTTP_202_ACCEPTED)
def update_data(uid: int, params: dict):
    try:
        if 'availableTime' in params.keys() != None:
            if 'bandwidth' not in params.keys():
                return {'missing': 'bandwidth'}
            time = params.get('availableTime')
            params['availableTime'] = [
                convert24(time[0].strip()), convert24(time[1].strip())]
            data = {
                'uid': uid, 'availableTime': params['availableTime'], 'bandwidth': params['bandwidth']}
            if params.get('btp') == True:
                database.tripPlanner(DB_URL, DB_HEADERS).add(**data)
            if params.get('bta') == True:
                database.tripAssistance(DB_URL, DB_HEADERS).add(**data)
            if params.get('blg') == True:
                database.localGuide(DB_URL, DB_HEADERS).add(**data)

        else:
            if params.get('blg') == True:
                bandwidth = users.show(uid=uid)[0]['bandwidth']
                timing = users.show(uid=uid)[0]['availableTime']
                data = {'uid': uid, 'availableTime': timing,
                        'bandwidth': bandwidth}
                database.localGuide(DB_URL, DB_HEADERS).add(**data)
            if params.get('btp') == True:
                bandwidth = users.show(uid=uid)[0]['bandwidth']
                timing = users.show(uid=uid)[0]['availableTime']
                data = {'uid': uid, 'availableTime': timing,
                        'bandwidth': bandwidth}
                database.tripPlanner(DB_URL, DB_HEADERS).add(**data)
            if params.get('bta') == True:
                bandwidth = users.show(uid=uid)[0]['bandwidth']
                timing = users.show(uid=uid)[0]['availableTime']
                data = {'uid': uid, 'availableTime': timing,
                        'bandwidth': bandwidth}
                database.tripAssistance(DB_URL, DB_HEADERS).add(**data)

            if params.get('bta') == False:
                database.tripAssistance(DB_URL, DB_HEADERS).delete(uid=uid)
            if params.get('btp') == False:
                database.tripPlanner(DB_URL, DB_HEADERS).delete(uid=uid)
            if params.get('blg') == False:
                database.localGuide(DB_URL, DB_HEADERS).delete(uid=uid)

        response = users.update(uid, **params)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.delete('/delete/{uid}', status_code=status.HTTP_204_NO_CONTENT)
def delete_User(uid: int):
    users.delete(uid=uid)
    return {'detail': 'done'}
