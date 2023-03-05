from .. import *
from ..admin.credentials import MID, KEY, CLIENT_ID, WEBSITE, CALLBACK_URL, ENVIRONMENT
from ..models.payment import tokenInfo, Refund


router = FastAPI()


# Find your mid, key, website in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
paytmpg.MerchantProperty.set_callback_url(CALLBACK_URL)
paytmpg.MerchantProperty.initialize(ENVIRONMENT, MID, KEY, CLIENT_ID, WEBSITE)


@router.post('/token')
async def getToken(params: tokenInfo):
    params = params.dict()
    orderId = str(uuid4())
    txn_amount = paytmpg.Money(params['CURRENCY'], params['AMOUNT'])
    user_info = paytmpg.UserInfo()
    user_info.set_cust_id(params["CUSTOMER_ID"])
    user_info.set_first_name(params["CUSTOMER_FIRST_NAME"])
    user_info.set_last_name(params["CUSTOMER_LAST_NAME"])
    user_info.set_mobile(params["CUSTOMER_MOBILE_NO"])
    payment_details = paytmpg.PaymentDetailsBuilder(
        params['CHANNEL_ID'], orderId, txn_amount, user_info).build()
    return paytmpg.Payment.createTxnToken(payment_details).get_json_response()


@router.get('/order-status/{orderId}')
async def orderStatus(orderId):
    read_timeout = 30*1000
    payment_status_detail = paytmpg.PaymentStatusDetailBuilder(
        orderId).set_read_timeout(read_timeout).build()
    return paytmpg.Payment.getPaymentStatus(payment_status_detail).get_json_response()


@router.post('/refund')
async def refundRequest(params: Refund):
    params = params.dict()
    txn_type = "REFUND"
    refund = paytmpg.RefundDetailBuilder(
        params['order_id'], params['ref_id'], params['txnId'], txn_type, params['refund_amount']).build()
    return paytmpg.Refund.doRefund(refund).get_json_response()


@router.get('/refund-status/{orderId}')
async def orderStatus(orderId: str, refId=str):
    refund_status_details = paytmpg.RefundStatusDetailBuilder(
    ).set_order_id(orderId).set_ref_id(refId).build()
    return paytmpg.Refund.getRefundStatus(refund_status_details).get_json_response()
