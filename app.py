from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nagad User Check</title>
        <link href="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
                font-family: 'Arial', sans-serif;
            }
            .container {
                margin-top: 50px;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            }
            .card {
                border: none;
                border-radius: 15px;
                animation: fadeIn 0.5s ease-in;
            }
            .form-control {
                border-radius: 10px;
            }
            .btn-primary {
                border-radius: 10px;
                transition: background-color 0.3s;
            }
            .btn-primary:hover {
                background-color: #007bff;
                transform: scale(1.05);
            }
            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card mt-5">
                        <div class="card-body">
                            <h2 class="text-center mb-4">Check Nagad User Status</h2>
                            <form action="/check_user" method="get">
                                <div class="mb-3">
                                    <label for="nagad_number" class="form-label">Enter NAGAD Number:</label>
                                    <input type="text" id="nagad_number" name="nagad_number" class="form-control" placeholder="e.g., 01234567890" required>
                                </div>
                                <div class="text-center">
                                    <button type="submit" class="btn btn-primary w-100">Submit</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.min.js"></script>
    </body>
    </html>
    '''

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
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>User Information</title>
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="text-center">User Information</h1>
                <div class="card mt-4">
                    <div class="card-body">
                        <p><strong>Name:</strong> {data.get('name', 'N/A')}</p>
                        <p><strong>User ID:</strong> {data.get('userId', 'N/A')}</p>
                        <p><strong>Status:</strong> {data.get('status', 'N/A')}</p>
                        <p><strong>User Type:</strong> {data.get('userType', 'N/A')}</p>
                        <p><strong>RB Base:</strong> {data.get('rbBase', 'N/A')}</p>
                        <p><strong>Auth Token Info:</strong> {data.get('authTokenInfo', 'N/A')}</p>
                        <p><strong>Verification Status:</strong> {data.get('verificationStatus', 'N/A')}</p>
                        <p><strong>Execution Status:</strong> {data.get('executionStatus', 'N/A')}</p>
                        <a href="/" class="btn btn-primary">Back</a>
                    </div>
                </div>
            </div>
            
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.0/js/bootstrap.min.js"></script>
        </body>
        </html>
        '''
    else:
        return f"Error: {response.status_code}, {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
