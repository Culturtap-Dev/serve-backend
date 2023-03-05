import time
from ..classes.database import database
from ..admin.credentials import DB_URL, DB_HEADERS
from ..routers.userAPI import users, get_data_by_location
import socketio

sio = socketio.AsyncServer(
    async_mode='asgi', cors_allowed_origins=[])
appIO = socketio.ASGIApp(socketio_server=sio)

chatApp = database.Chat(DB_URL, DB_HEADERS)

usersId = {}
msg = {}


@sio.on('connect')
async def connect(sid, environ, auth):
    print('connected sid :', sid)
    usersId[sid] = (None, None)


@sio.event
async def disconnect(sid):
    print('disconnected sid :', sid)
    if sid in usersId.keys():
        if None not in usersId[sid]:
            userInfo=usersId.get(sid)
            if len(userInfo)==4:
                uid, room, name, phoneNo=userInfo
                message = {"uid": uid, "name": name, "msg": "exit",
                        'timestamp': time.strftime("%Y-%m-%d %H:%M %z")}
                msg[room].append(message)
                chatApp.update(
                    room=room, messages=msg[room], completedOn=message['timestamp'])
                data = {'name': name, "room": room}
                await sio.emit('leave-room', data=data, room=room)
    del usersId[sid]
    


@sio.on('add-user')
async def addUser(sid, uid):
    try:
        userData = users.show(uid=int(uid))[0]
        name = userData['name']
        phoneNo = f"{userData['countryCode']}{userData['phoneNo']}"
        usersId[sid] = (int(uid), name, phoneNo)
    except IndexError:
        name = 'null'

    await sio.emit('add-user', data={"uid": uid, 'name': name}, to=sid)


@sio.on('send-request')
async def sendRequest(sid, data):
    currentUID = usersId.get(sid)[0]
    availableUsers = get_data_by_location(
        currentUID=currentUID, maxKm=20, filtor={'bta': True})
    for user in availableUsers:
        connectedUsers = [(key,user['distance']) for key,
                          value in usersId.items() if value[0] == user['uid']]
    for key in connectedUsers:
        data['distance']=key[1]
        await sio.emit('get-request', data=data, to=key[0])
    await sio.emit('request-response', data=len(connectedUsers), to=sid)


@sio.on('create-room')
async def createRoom(sid):
    try:
        uid, name, phoneNo = usersId[sid]
        usersId[sid] = (uid, sid, name, phoneNo)
        room = sid
        msg[room] = []
        sio.enter_room(sid=room, room=room)
        chatApp.add(room=room, user1=int(uid), by=name,
                    createdOn=time.strftime("%Y-%m-%d %H:%M %z"))
        await sio.emit('create-room', data=room, to=room)
    except:
        await sio.emit('create-room', data='invalid...', to=sid)


@sio.on('join-room')
async def joinRoom(sid, room):
    try:
        count = 0
        for value in usersId.values():
            if value[1] == room:
                count += 1

        if count < 2:
            uid, name, phoneNo = usersId[sid]
            usersId[sid] = (uid, sid, name, phoneNo)
            message = {"uid": uid, "name": name, "msg": "join",
                       'timestamp': time.strftime("%Y-%m-%d %H:%M %z")}

            sio.enter_room(sid, room)

            chatApp.update(room=room, user2=uid, with_=name)
            msg[room].append(message)

            await sio.emit("join-room", name, room=room)
        else:
            await sio.emit("join-room", "already full...", to=sid)
    except:
        await sio.emit('join-room', data='invalid...', to=sid)


@sio.on('send-msg')
async def message(sid, message):
    uid, room, name, phoneNo = usersId.get(sid)
    timestamp = time.strftime("%Y-%m-%d %H:%M %z")
    data = {"uid": uid, 'name': name,
            "message": message, "timestamp": timestamp}
    msg[room].append(data)
    await sio.emit(event='send-msg', data=data, room=room)


@sio.on('drop-room')
async def dropRoom(sid, room):
    await sio.close_room(room)
    for key, value in usersId.items():
        if value[1] == room:
            del usersId[key]
            await sio.disconnect(key)


async def response(uid: int, msg: str):
    for sid, value in usersId.items():
        if value[0] == str(uid):
            await sio.emit('ping', msg, to=sid)
            break
'''
data : {
        uid:str/int,
        room:str
    }
'''

# message : str

'''
room : str
user1 : int
by : str
createdOn : str
messages : list[dict]
user2 : int
with_ : str
completedOn : str
'''
