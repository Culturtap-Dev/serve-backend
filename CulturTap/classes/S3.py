class Boto3:
    def __init__(self, access_key: str, secret_key: str, bucket: str) -> None:
        import boto3
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )
    def upload(self, file:bytes, key: str, folder: str, bucket:str):
        key = folder+key
        self.client.put_object(Bucket=bucket, Body=file, Key=key,ACL='public-read')
    
    def delete(self, bucket:str,key:str):
        self.client.delete_object(Bucket=bucket, Key=key)