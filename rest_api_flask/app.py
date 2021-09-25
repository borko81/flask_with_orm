from flask import Flask, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(255))

    def __init__(self, title, content):
        self.title = title
        self.content = content


class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route('/note/')
def note_list():
    all_notes = NoteModel.query.all()
    return jsonify(all_notes)


@app.route('/note/', methods=['POST'])
def create_note():
    title = request.json.get('title', '')
    content = request.json.get('content', '')

    note = NoteModel(title=title, content=content)
    db.session.add(note)
    db.session.commit()

    return note_schema.jsonify(note)


if __name__ == "__main__":
    app.run(debug=True)
