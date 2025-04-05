from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tree_id = db.Column(db.Integer, db.ForeignKey('tree.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(100))
    option_b = db.Column(db.String(100))
    option_c = db.Column(db.String(100))
    option_d = db.Column(db.String(100))

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tree_id = db.Column(db.Integer, db.ForeignKey('tree.id'))
    submission_date = db.Column(db.Date, default=datetime.utcnow)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    selected_option = db.Column(db.String(1))  # A, B, C, or D
