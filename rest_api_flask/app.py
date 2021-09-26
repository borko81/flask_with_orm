from flask import Flask, json, jsonify, request
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app)


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


# Author and book
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="books")


# Marshmallow shema
class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author

    id = ma.auto_field()
    name = ma.auto_field()
    books = ma.auto_field()


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route('/note/', methods=['GET'])
def note_list():
    all_notes = NoteModel.query.all()
    notes_schema = NoteSchema(many=True)
    data = notes_schema.dump(all_notes)
    return jsonify({'result': data})


@app.route('/note/<id>', methods=['GET'])
def note_detail(id):
    note = NoteModel.query.filter_by(id=id).first_or_404()
    note_schema = NoteSchema()
    data = note_schema.dump(note)
    return jsonify({'result': data})


@app.route('/author', methods=['GET'])
def get_authors():
    a = Author.query.all()
    s = AuthorSchema(many=True)
    data = s.dump(a)
    return jsonify({'authores': data})


@app.route('/books', methods=['GET'])
def get_books():
    b = Book.query.all()
    s = BookSchema(many=True)
    data = s.dump(b)
    return jsonify({'books': data})


if __name__ == "__main__":
    app.run(debug=True)
