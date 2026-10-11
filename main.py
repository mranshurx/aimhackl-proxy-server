import os
import base64
from flask import Flask, Response, request

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 10000))

# Your static VLESS node configuration string
VLESS_NODE = "vless://b831381d-6324-4d53-ad4f-8cda48b30811@aimhackl-proxy-server.onrender.com:443?encryption=none&type=ws&path=/intercept#CYBER-ENGINE-Cloud"

# Endpoint 1: Serves as a valid V2Ray/Happ Subscription URL
@app.route('/sub', methods=['GET'])
def subscription():
    # Base64 encode the config so Happ can parse it seamlessly
    encoded_sub = base64.b64encode(VLESS_NODE.encode('utf-8')).decode('utf-8')
    return Response(encoded_sub, mimetype='text/plain')

# Endpoint 2: Interceptor endpoint for traffic inspection
@app.route('/intercept', methods=['GET', 'POST'])
def intercept():
    if request.method == 'POST':
        data = request.get_data()
        print(f"[CLOUD PACKET] Received {len(data)} bytes")
    return "OK", 200

@app.route('/', methods=['GET'])
def home():
    return "CYBER-ENGINE Node Server Active", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
