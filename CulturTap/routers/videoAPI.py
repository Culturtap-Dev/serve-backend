from .. import *
from ..utils import *
from ..classes.database import database
from ..classes.S3 import Boto3
from ..models.videos import videoModel_View, videoModel_Post, s3Response
from ..admin.credentials import DB_URL, DB_HEADERS, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, TOKEN
from ..constants import BUCKET, VIDEOS, FILETYPES

router = APIRouter(prefix='/videos', tags=['Videos'])
user = database.Users(DB_URL, DB_HEADERS)
# --VIDEO DATA
client = database.Videos(url=DB_URL, header=DB_HEADERS)
s3 = Boto3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET)


@router.get("/get", status_code=status.HTTP_200_OK, response_model=list[videoModel_View])
def get_all_videos(token: str, end: int, start: int = 0):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        if start == 0:
            start += 1
        return client.show()[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/get/video/{videoId}", status_code=status.HTTP_200_OK, response_model=videoModel_View)
def get_video_by_videoId(videoId: int):
    try:
        return client.show(videoId=videoId)[0]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/get/user/{uid}", status_code=status.HTTP_200_OK, response_model=list[videoModel_View])
def get_videos_by_uid(uid: int, end: int, start: int = 0):
    try:
        return client.show(uid=uid)[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/get/matching", status_code=status.HTTP_200_OK, response_model=list[videoModel_View])
def get_data_by_matching(token: str, params: dict, end: int, start: int = 0):
    if token != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid')
    try:
        return client.show(**params)[start:end]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/get/by-distance/uid={CurrentUID}", status_code=status.HTTP_200_OK, response_model=list[videoModel_View])
def get_data_by_location(CurrentUID: int, maxKm: float, filtor: dict, minKm: float = 0):
    try:
        videos = []
        User = user.show(uid=CurrentUID)[0]
        lat1, long1 = round(User['lat'], 2), round(User['long'], 2)
        for i in client.show(**filtor):
            lat2, long2 = round(i['lat'], 2), round(i['long'], 2)
            if minKm <= lat_long_difference((lat2, long2), (lat1, long1)) >= maxKm:
                videos.append(i)
        return videos
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/add', status_code=status.HTTP_201_CREATED)
def adding_video_content(params: videoModel_Post):
    params = params.dict()
    try:
        return client.add(**params)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/add-video', status_code=status.HTTP_200_OK, response_model=s3Response)
async def adding_video(videoId: int, video: list[UploadFile], action: str = "add"):
    try:
        toUpdate = {}
        videoData = get_video_by_videoId(videoId)
        videos_keys = []
        urls = []

        for item in video:
            if item.content_type in FILETYPES:
                key = f'{uuid4()}.{FILETYPES[item.content_type]}'
                data = await item.read()
                s3.upload(file=data, key=key, folder=VIDEOS, bucket=BUCKET)
                url = f'https://{BUCKET}.s3.ap-south-1.amazonaws.com/{VIDEOS}{key}'
                urls.append(url)
                videos_keys.append(f"{VIDEOS}{key}")

        if action.lower() == 'add':
            existingPic = videoData['url']
            urls += existingPic
        else:
            if keys := videoData.get('videoKeys'):
                for i in keys:
                    s3.delete(bucket=BUCKET, key=i)

        toUpdate['url'] = urls
        toUpdate['videoKeys'] = videos_keys
        update_video(videoId, toUpdate)
        return toUpdate
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.patch('/update/{videoId}', status_code=status.HTTP_202_ACCEPTED)
def update_video(videoId: int, params: dict):
    try:
        try:
            Likes = database.likes(DB_URL, DB_HEADERS)
            if params.get('views') != None:
                params['views'] = client.show(videoId=videoId)[
                    0]["views"]+params['views']

            likes = params.get('likes')
            if likes != None:
                if len(Likes.show(User=params['User'], videoId=videoId)) != 0:
                    video = client.show(videoId=videoId)[0]
                    if likes == 1:
                        params['likes'] = video["likes"]+likes
                        Likes.add(User=params['User'], videoId=videoId)
                    elif likes != 1:
                        params['likes'] = video["likes"]-likes
                        Likes.delete(User=params['User'], videoId=videoId)
                    del params['User']
                else:
                    return {'msg': 'already liked by the user...'}
        except:
            pass
        response = client.update(videoId, **params)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.delete('/delete/{videoId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_video(videoId: int):
    Likes = database.likes(DB_URL, DB_HEADERS)
    Likes.deleteMany(videoId=videoId)
    videoData = get_video_by_videoId(videoId)
    if keys := videoData.get('videoKeys'):
        for i in keys:
            s3.delete(bucket=BUCKET, key=i)
    client.delete(videoId=videoId)
    return {'detail': 'done'}
