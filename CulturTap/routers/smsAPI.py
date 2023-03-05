from .. import *
from ..classes.smsText import SMS
from ..models.sms import messageModel, OTPmodel
from ..admin.credentials import SMSID, SMSTOKEN

router = APIRouter(prefix='/sms', tags=['SMS'])

# --SMS

client = SMS(auth_id=SMSID, auth_token=SMSTOKEN)


@router.post('/msg', status_code=status.HTTP_201_CREATED)
def send_sms(params: messageModel):
    params = params.dict()
    params['phoneNo'] = params['countryCode']+str(params['phoneNo'])
    return client.send_sms(to=params['phoneNo'], body=params['msg'], by='CulturTap')


@router.get('/otp/{phoneNo}', status_code=status.HTTP_201_CREATED, response_model=OTPmodel)
def send_OTP(phoneNo: str):
    return client.send_otp(to=phoneNo, org='CulturTap')
