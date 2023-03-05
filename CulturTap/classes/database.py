from .. import *

# Managing database


class database:
    def __init__(self, url: str, header: dict) -> None:
        self.url = url
        self.headers = header

    def find(self, collection: str, **params):
        endpoint = 'find'
        payload = dumps({
            "collection": collection,
            "database": "Culturtap",
            "dataSource": "CulturTap",
            "filter": params
        })
        return requests.request("POST", url=self.url+endpoint, headers=self.headers, data=payload).json()

    def updateOne(self, collection: str, params: dict, **updates):
        endpoint = 'updateOne'
        payload = dumps({
            "collection": collection,
            "database": "Culturtap",
            "dataSource": "CulturTap",
            "filter": params,
            "update": {'$set': updates}
        })
        return requests.request("POST", url=self.url+endpoint, headers=self.headers, data=payload).json()

    def insertOne(self, collection: str, **params):
        endpoint = 'insertOne'
        payload = dumps({
            "collection": collection,
            "database": "Culturtap",
            "dataSource": "CulturTap",
            "document": params,
        })
        return requests.request("POST", url=self.url+endpoint, headers=self.headers, data=payload).json()

    def deleteOne(self, collection: str, **params):
        endpoint = 'deleteOne'
        payload = dumps({
            "collection": collection,
            "database": "Culturtap",
            "dataSource": "CulturTap",
            "filter": params
        })
        return requests.request("POST", url=self.url+endpoint, headers=self.headers, data=payload).json()

    def deleteMany(self, collection: str, **params):
        endpoint = 'deleteMany'
        payload = dumps({
            "collection": collection,
            "database": "Culturtap",
            "dataSource": "CulturTap",
            "filter": params
        })
        return requests.request("POST", url=self.url+endpoint, headers=self.headers, data=payload).json()

    class Users:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Users'

        def add(self, **jsonData):
            self.id = self.client.find(collection=self.collection, field='cursor_at_uid')[
                'documents'][0]['value']
            jsonData['uid'] = self.id
            self.client.updateOne(collection=self.collection, params={
                'field': 'cursor_at_uid'}, value=self.id+1)
            self.client.insertOne(collection=self.collection, **jsonData)
            return {'uid': jsonData['uid']}

        def show(self, **params):
            return self.client.find(collection=self.collection, **params)['documents']

        def update(self, uid: int, **updates):
            return self.client.updateOne(collection=self.collection, params={'uid': uid}, **updates)

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)

        def matchUserDetail(self, **params):
            if len(doc := self.client.find(collection=self.collection, **params)['documents']) > 0:
                self.uid = doc[0]['uid']
                return True
            return False

    class Videos:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Videos'

        def add(self, **jsonData):
            self.id = self.client.find(collection=self.collection, field='cursor_at_videoId')[
                'documents'][0]['value']
            jsonData['videoId'] = self.id
            self.client.updateOne(collection=self.collection, params={
                'field': 'cursor_at_videoId'}, value=self.id+1)
            self.client.insertOne(collection=self.collection, **jsonData)
            return {'uid': jsonData['uid'], 'videoId': jsonData['videoId']}

        def show(self, **params):
            return self.client.find(collection=self.collection, **params)['documents']

        def update(self, videoId: int, **updates):
            return self.client.updateOne(collection=self.collection, params={'videoId': videoId}, **updates)

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)

        def matchVideoDetail(self, **params):
            if len(doc := self.client.find(collection=self.collection, **params)['documents']) > 0:
                self.uid = doc['uid']
                self.videoId = doc['videoId']
                return True
            return False

    class likes:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Likes'

        def add(self, **jsonData):
            return self.client.insertOne(collection=self.collection, **jsonData)

        def show(self, **params):
            return self.client.find(collection=self.collection, **params)['documents']

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)

        def deleteMany(self, **params):
            return self.client.deleteMany(collection=self.collection, **params)

    class expertCard:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Expert Card'

        def add(self, **jsonData):
            self.client.insertOne(collection=self.collection, **jsonData)
            return {'uid': jsonData['uid']}

        def show(self, **params):
            return self.client.find(collection=self.collection, **params)['documents']

        def update(self, uid: int, **updates):
            return self.client.updateOne(collection=self.collection, params={'uid': uid}, **updates)

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)

        def matchExpertDetail(self, **params):
            if len(doc := self.client.find(collection=self.collection, **params)['documents']) > 0:
                self.uid = doc['uid']
                return True
            return False

    class tripPlanner:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Trip Planner'

        def add(self, **jsonData):
            self.client.insertOne(collection=self.collection, **jsonData)
            return {'uid': jsonData['uid']}

        def show(self, **params):
            return self.client.find(collection=self.collection, **params)['documents']

        def update(self, uid: int, **updates):
            return self.client.updateOne(collection=self.collection, params={'uid': uid}, **updates)

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)

    class tripAssistance:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Trip Assistance'

        def add(self, **jsonData):
            self.client.insertOne(collection=self.collection, **jsonData)
            return {'uid': jsonData['uid']}

        def show(self, **params):
            return self.client.find(collection=self.collection, **params)['documents']

        def update(self, uid: int, **updates):
            return self.client.updateOne(collection=self.collection, params={'uid': uid}, **updates)

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)

    class localGuide:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Local Guide'

        def add(self, **jsonData):
            self.client.insertOne(collection=self.collection, **jsonData)
            return {'uid': jsonData['uid']}

        def show(self, **params):
            return self.client.find(collection=self.collection, **params)['documents']

        def update(self, uid: int, **updates):
            return self.client.updateOne(collection=self.collection, params={'uid': uid}, **updates)

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)

    class Calls:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Scheduled Calls'

        def add(self, **jsonData):
            return self.client.insertOne(collection=self.collection, **jsonData)

        def show(self, **params):
            data = []
            for i in self.client.find(collection=self.collection, **params)['documents']:
                i['callId'] = i['_id']
                del i['_id']
                data.append(i)
            return data

        def update(self, params: dict, **updates):
            return self.client.updateOne(collection=self.collection, params=params, **updates)

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)

    class Chat:
        def __init__(self, url: str, header: dict) -> None:
            self.client = database(url, header)
            self.collection = 'Chats'

        def add(self, **jsonData):
            self.client.insertOne(collection=self.collection, **jsonData)
            return {'room': jsonData['room']}

        def show(self, **params):
            return self.client.find(collection=self.collection, **params)['documents']

        def update(self, room, **updates):
            return self.client.updateOne(collection=self.collection, params={'room': room}, **updates)

        def delete(self, **params):
            return self.client.deleteOne(collection=self.collection, **params)
