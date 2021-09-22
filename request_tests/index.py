from flask import Flask

app = Flask(__name__)

state = ''


@app.before_request
def before_request():
    global state
    state += 'This is state'


@app.after_request
def after_request(response):
    print(response.status_code)
    return response


@app.route('/')
def index():
    return {'status': state}


if __name__ == '__main__':
    app.run(debug=True)
