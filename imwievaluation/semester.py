import sqlalchemy as db
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import relationship
from base import Base


class Semester(Base):
    __tablename__ = 'semester'

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(mysql.ENUM('WS', 'SS'), nullable=False)
    year = db.Column(mysql.YEAR(), nullable=False)

    # prevent duplicate entries
    db.UniqueConstraint(term, year)

    # one two many relationship between semester and lecture
    lectures = relationship("Lecture", back_populates="semester")

    def __init__(self, term, year):
        self.term = term
        self.year = year

    def __str__(self):
        return '%s%s' % (self.term, self.year)
