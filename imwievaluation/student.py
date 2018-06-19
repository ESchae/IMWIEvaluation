import sqlalchemy as db
from base import Base


class Student(Base):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    email = db.Column(db.String(30))

    # prevent duplicate entries
    db.UniqueConstraint(first_name, last_name, email)

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
