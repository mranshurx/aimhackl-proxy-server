import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Render provides the port via the PORT environment variable
PORT = int(os.environ.get("PORT", 10000))

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "CYBER-ENGINE Cloud Proxy Active",
        "node": "Render Edge"
    })

# Endpoint to inspect incoming packet payloads from phone
@app.route('/intercept', methods=['POST'])
def intercept():
    packet_data = request.get_data()
    print(f"\n[CLOUD PACKET CAPTURED] Length: {len(packet_data)} bytes")
    print(packet_data[:300]) # Log packet data directly to Render dashboard logs
    
    # Return response back to phone
    return jsonify({"status": "received", "bytes": len(packet_data)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
