import uvicorn
import socketio
from fastapi import FastAPI

# สร้าง Socket.IO Server และ FastAPI App
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app.mount('/', socketio.ASGIApp(sio))

# เก็บข้อมูลผู้เล่นทั้งหมดในเซิร์ฟเวอร์
players = {}

@sio.event
async def connect(sid, environ):
    print(f"[+] ผู้เล่นเชื่อมต่อ: {sid}")
    players[sid] = {
        "id": sid,
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
        "rot": 0.0,
        "action": "stand"
    }
    await sio.emit('update_players', players)

@sio.event
async def player_move(sid, data):
    """ รับข้อมูลพิกัดและการเคลื่อนไหวจากผู้เล่น """
    if sid in players:
        players[sid]["x"] = data.get("x", 0.0)
        players[sid]["y"] = data.get("y", 0.0)
        players[sid]["z"] = data.get("z", 0.0)
        players[sid]["rot"] = data.get("rot", 0.0)
        players[sid]["action"] = data.get("action", "stand")
        
        await sio.emit('update_players', players)

@sio.event
async def disconnect(sid):
    print(f"[-] ผู้เล่นออกจากการเชื่อมต่อ: {sid}")
    if sid in players:
        del players[sid]
    await sio.emit('update_players', players)

if __name__ == '__main__':
    uvicorn.run('server:app', host='0.0.0.0', port=8000, reload=True)
