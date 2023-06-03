from flask import Flask, request
from datetime import datetime, timedelta

app = Flask(__name__)

LIMIT_PERIOD = timedelta(minutes=1)

LIMIT_REQUESTS = 100

request_counts = {}

@app.before_request
def apply_request_limit():
    client_ip = request.remote_addr

    if client_ip in request_counts:
        last_request_time = request_counts[client_ip][0]

        if datetime.now() - last_request_time < LIMIT_PERIOD:
            count = request_counts[client_ip][1]
            if count >= LIMIT_REQUESTS:
                return 'Too Many Requests', 429

            request_counts[client_ip][1] += 1
        else:
            request_counts[client_ip] = [datetime.now(), 1]
    else:
        request_counts[client_ip] = [datetime.now(), 1]


@app.route('/')
def hello_world():
    return 'Your website shit or etc what do you want'

if __name__ == '__main__':
    app.run(port=80)
