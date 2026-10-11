import os
import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse

app = FastAPI()

# Your VLESS subscription payload string
VLESS_NODE = "vless://b831381d-6324-4d53-ad4f-8cda48b30811@aimhackl-proxy-server.onrender.com:443?security=tls&encryption=none&type=ws&path=/intercept&fp=chrome#CYBER-ENGINE-Cloud"

@app.get("/")
async def home():
    return {"status": "CYBER-ENGINE Interceptor Active"}

@app.get("/sub")
async def subscription():
    encoded_sub = base64.b64encode(VLESS_NODE.encode('utf-8')).decode('utf-8')
    return PlainTextResponse(encoded_sub)

# WebSocket Interceptor endpoint matching your VLESS path
@app.websocket("/intercept")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("\n[+] SUCCESS: Happ WebSocket Connection Established!")
    
    packet_count = 0
    try:
        while True:
            # Receive incoming data packets from your phone in real-time
            data = await websocket.receive_bytes()
            packet_count += 1
            print(f"[PACKET #{packet_count}] Captured {len(data)} bytes from phone.")
            
            # Echo/forward response back to keep the connection healthy and stable
            await websocket.send_bytes(data)
            
    except WebSocketDisconnect:
        print("[-] WebSocket Connection Closed by Client.")
    except Exception as e:
        print(f"[!] WebSocket Error: {e}")
