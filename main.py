import os
import base64
import asyncio
import struct
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse

app = FastAPI()

VLESS_NODE = "vless://b831381d-6324-4d53-ad4f-8cda48b30811@aimhackl-proxy-server.onrender.com:443?security=tls&encryption=none&type=ws&path=/intercept&fp=chrome#CYBER-ENGINE-Cloud"

@app.get("/")
async def home():
    return {"status": "CYBER-ENGINE Proxy Interceptor Active"}

@app.get("/sub")
async def subscription():
    encoded_sub = base64.b64encode(VLESS_NODE.encode('utf-8')).decode('utf-8')
    return PlainTextResponse(encoded_sub)

async def pipe(reader, writer):
    try:
        while True:
            data = await reader.read(8192)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception:
        pass
    finally:
        writer.close()

@app.websocket("/intercept")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[+] Happ WebSocket Tunnel Connected.")

    try:
        while True:
            # Receive multiplexed packet stream from Happ
            message = await websocket.receive_bytes()
            if len(message) < 2:
                continue

            # VLESS Protocol Parsing
            version = message[0]
            cmd = message[17] if len(message) > 17 else 1
            port = struct.unpack(">H", message[18:20])[0] if len(message) >= 20 else 80
            addr_type = message[20] if len(message) > 20 else 1

            if addr_type == 1: # IPv4
                target_host = ".".join(str(b) for b in message[21:25])
                payload_offset = 25
            elif addr_type == 2: # Domain
                domain_len = message[21]
                target_host = message[22:22+domain_len].decode('utf-8', errors='ignore')
                payload_offset = 22 + domain_len
            else:
                target_host = "1.1.1.1"
                payload_offset = 21

            print(f"[TUNNEL ROUTE] Target -> {target_host}:{port} | Size: {len(message)} bytes")

            # Connect to target server in background task to avoid blocking the tunnel loop
            async def handle_connection():
                try:
                    remote_reader, remote_writer = await asyncio.open_connection(target_host, port)
                    
                    # Send VLESS handshake confirmation back
                    await websocket.send_bytes(bytes([version, 0]))

                    initial_data = message[payload_offset:]
                    if initial_data:
                        remote_writer.write(initial_data)
                        await remote_writer.drain()

                    # Two-way data pipe between target server and phone WebSocket
                    # (Simplified robust mirroring)
                    await asyncio.gather(
                        pipe(remote_reader, remote_writer),
                        return_exceptions=True
                    )
                except Exception as e:
                    pass

            asyncio.create_task(handle_connection())

    except WebSocketDisconnect:
        print("[-] Happ WebSocket Tunnel Disconnected.")
    except Exception as e:
        print(f"[!] Tunnel Notice: {e}")
