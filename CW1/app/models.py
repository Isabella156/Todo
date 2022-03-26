from app import db


# todo table for storing assessments
class Todo(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    deadline = db.Column(db.DateTime)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    complete = db.Column(db.Boolean)
    # test migrate
    # test = db.Column(db.Integer)


# code table for storing codes of all assessments
class Code(db.Model):
    __tablename__ = 'code'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))


# title table for storing titles of all assessments
class Title(db.Model):
    __tablename__ = 'title'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
