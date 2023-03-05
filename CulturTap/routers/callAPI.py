from .. import *
from ..classes.database import database
from ..models.scheduleCall import scheduleCall, scheduleCallAdd, scheduleCallAddResponse, msgCall
from ..admin.credentials import DB_URL, DB_HEADERS, TOKEN
from ..utils import convert24
from ..chat.sockets import response

router = APIRouter(prefix='/call', tags=['Schedule Calls'])
user = database.Users(DB_URL, DB_HEADERS)

# --CALL DATA
client = database.Calls(url=DB_URL, header=DB_HEADERS)


@router.post("/get", status_code=status.HTTP_200_OK, response_model=list[scheduleCall])
def get_Calls(params: dict, token=str):
    if token != TOKEN:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Token is not valid')
    try:
        return client.show(**params)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/add', status_code=status.HTTP_201_CREATED, response_model=Union[scheduleCallAddResponse, msgCall])
async def add_call(params: scheduleCallAdd):
    params = params.dict()
    try:
        # from
        date, from_, period = params['from_'].split()
        yearF, monthF, dayF = date.strip().split('-')
        from_ = from_+period
        from_ = convert24(from_.strip())
        params['from_'] = date+' '+from_

        # to
        dateT, to, period = params['to'].split()
        yearT, monthT, dayT = date.strip().split('-')
        to = to+period
        to = convert24(to)
        params['to'] = dateT+' '+to

        # checking within Scheduled calls
        request = {
            "requestTo": params['requestTo'],
            "status": "scheduled"
        }
        userData = user.show(uid=params['requestTo'])[0]
        userFrom, userTo = userData['availableTime']
        params['toUser'] = userData['name']
        params['fromUser'] = userData['name']
        period = DateTimeRange(userFrom, userTo)
        userBandwidth = userData['bandwidth']
        if userBandwidth == 'daily':
            if from_ in period and to in period:
                if len(calls := get_Calls(request,token=TOKEN)) != 0:
                    for i in calls:
                        range_ = DateTimeRange(i['from_'], i['to'])
                        if date+' '+from_ in range_ or dateT+' '+to in range_:
                            return {'msg': 'not possible'}
            else:
                return {'msg': 'check available time'}
        else:
            if calendar.weekday(year=int(yearF), month=int(monthF), day=int(dayF)) in [1, 2, 3, 4] or calendar.weekday(year=int(yearT), month=int(monthT), day=int(dayT)) in [1, 2, 3, 4]:
                return {'msg': 'check bandwidth'}

            if from_ in period and to in period:
                if len(calls := get_Calls(request, token=TOKEN)) != 0:
                    for i in calls:
                        range_ = DateTimeRange(i['from_'], i['to'])
                        if date+' '+from_ in range_ or dateT+' '+to in range_:
                            return {'msg': 'not possible'}
            else:
                return {'msg': 'check available time'}

        # updating fields
        user.update(uid=params['requestTo'], pendingRequests=userData['pendingRequests'] +
                    1, totalRequests=userData['totalRequests']+1)
        userData = client.add(**params)
        userData['status'] = 'call added'
        await response(params['requestTo'], "call")
        return userData
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.patch('/update/{callId}', status_code=status.HTTP_202_ACCEPTED)
def update_call(callId: str, params: dict):
    try:
        response = client.update({'_id': ObjectId(callId)}, **params)
        dataId = client.show(_id=ObjectId(callId))[0]['requestTo']
        data = user.show(uid=dataId)[0]
        pendingRequests = data['pendingRequests']
        totalRequests = data['totalRequests']
        if params.get('status') == 'scheduled':
            if pendingRequests > 0:
                user.update(uid=dataId, pendingRequests=pendingRequests -
                            1, totalRequests=totalRequests+1)
            else:
                user.update(uid=dataId, totalRequests=totalRequests+1)
        elif params.get('status') == 'canceled':
            if totalRequests > 0:
                user.update(uid=dataId, pendingRequests=pendingRequests -
                            1, totalRequests=totalRequests-1)
            else:
                user.update(uid=dataId, pendingRequests=pendingRequests-1)
            return delete_call(callId)
        else:
            user.update(uid=dataId, pendingRequests=pendingRequests +
                        1, totalRequests=totalRequests+1)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST)


@router.delete('/delete/{callId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_call(callId: str):
    client.delete(_id=ObjectId(callId))
    return {'detail': 'deleted'}
