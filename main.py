from flask import Flask

app = Flask(__name__)


@app.route('/check')
def test_me():
    return "This is a check"


if __name__ == '__main__':
    app.run(debug=True)
