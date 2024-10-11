from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_user', methods=['GET'])
def check_user():
    suyaib = request.args.get('nagad_number')
    url = "https://app2.mynagad.com:20002/api/user/check-user-status-for-log-in"
    
    params = {'msisdn': suyaib}
    headers = {
        'X-KM-User-AspId': '100012345612345',
        'X-KM-User-Agent': 'ANDROID/1164',
        'X-KM-DEVICE-FGP': '5AB18952A962A31MM9A89524F6282F78905DDE9F94656B5C1CFCEDNN74AE660E',
        'X-KM-Accept-language': 'bn',
        'X-KM-AppCode': '01',
        'Host': 'app2.mynagad.com:20002',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.14.9'
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return render_template('result.html', data=data)
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
