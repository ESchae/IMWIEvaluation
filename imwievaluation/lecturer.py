import sqlalchemy as db
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship
from base import Base


class Lecturer(Base):
    __tablename__ = 'lecturer'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    gender = db.Column(mysql.ENUM('male', 'female'), nullable=False)

    db.UniqueConstraint('first_name', 'last_name')


    # one to many relationship between lecturer and lectures
    # compare with declaration in lecture.py
    lectures = relationship("Lecture", back_populates="lecturer")

    def __init__(self, first_name, last_name, email, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
