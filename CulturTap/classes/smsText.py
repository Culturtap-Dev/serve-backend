from .. import *

# Managing SMS


class SMS:
    id = None
    token = None

    def __init__(self, auth_id: str, auth_token: str) -> None:
        self.id = auth_id
        self.token = auth_token
        self.client = plivo.RestClient(auth_id=auth_id, auth_token=auth_token)

    def send_otp(self, to: str, org: str):
        self.to = to
        self.org = org
        self.otp = random.randint(1111, 9999)
        body = f"Hey,\nhere is your one-time password to login : {self.otp}\n- {self.org}"
        self.message = self.client.messages.create(
            src=self.org,
            dst=to,
            text=body,
        )
        return {"status": "SENT", "code": self.otp}

    def send_sms(self, to: str, body: str, by: str):
        body += '\n- CulturTap'
        self.client.messages.create(
            src=by,
            dst=to,
            text=body
        )
        return {"status": "SENT"}
