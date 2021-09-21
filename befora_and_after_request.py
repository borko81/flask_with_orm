from flask import Flask, session, g


app = Flask(__name__)
app.secret_key = '!123321!'


# Before each request
@app.before_request
def before_request_func():
    session['foo'] = 'bar'
    g.username = 'root'
    print("Before request")


@app.route('/')
def test_me():
    username = g.username
    foo = session.get('foo')
    print(username, foo)
    return "This is a check"


if __name__ == '__main__':
    app.run(debug=True)
