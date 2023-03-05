from .. import *


class tokenInfo(BaseModel):
    CUSTOMER_FIRST_NAME: str
    CUSTOMER_LAST_NAME: str
    CUSTOMER_MOBILE_NO: str
    CUSTOMER_ID: str
    CURRENCY: str = paytmpg.EnumCurrency.INR
    AMOUNT: str
    CHANNEL_ID: str = 'WAP'


class Refund(BaseModel):
    order_id: str
    ref_id: str
    txnId: str
    refund_amount: str
