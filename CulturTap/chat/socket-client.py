import socketio
import asyncio
client = socketio.AsyncClient()



async def main():
    await client.connect('http://localhost:8000/', socketio_path='/chat/socket.io')
    await client.wait()


@client.event
async def connect():
    print("I'm connected!")
    uid=int(input('uid : '))
    await client.emit('add-user',uid)
    

@client.on('add-user')
async def userAdd(myName):
    global MY_NAME
    MY_NAME=myName
    a = int(input('join ? '))
    if a == 1:
        data =input('room : ')
        await client.emit('join-room', data=data)

    else:
        await client.emit('create-room')





@client.on('create-room')
async def create(room):
    print("room :", room)


@client.on('join-room')
async def joinRoom(data):
    if data['name'].lower()!=MY_NAME.lower():
        print(f"{data['name']} joined the chat...")
    msg = input('me : ')
    await client.emit('send-msg', data=msg)


@client.on('send-msg')
async def msg(data):
    if data['name'].lower()!=MY_NAME.lower():
        print(f"{data['name']} : {data['message']}\ntimestamp : {data['timestamp']}")
    msg = input('me : ')
    await client.emit('send-msg', data=msg)


@client.on('leave-room')
async def leave(data):
    print(f'{data["name"]} left the chat...')
    # await sio.emit('drop-room',data["room"])


@client.event
async def disconnect():
    print("I'm disconnected!")

asyncio.get_event_loop_policy().get_event_loop().run_until_complete(main())
