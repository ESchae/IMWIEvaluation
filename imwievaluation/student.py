import sqlalchemy as db
from base import Base, UniqueMixin
from sqlalchemy.orm import relationship


class Student(Base):
    """
    WARNING: To be sure to have no duplicates in the database,
    class should be not instantiated via __init__, call
    Student.get_unique(...) instead.

    TODO: Maybe just catch duplications elsewere (IntegrityError...)
    TODO: This is not very intuitive, try to make this better
    See https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/UniqueObject
    Implicit constructor would be nice, but because then every class is
    decorated with a session which is e.g. taken from base.py
    problems arise when dealing with the session instantiated in the
    unittests... .

    """
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    # do not allow duplicate entries (should be not happen anyway because of
    # inheritance of UniqueMixin)
    db.UniqueConstraint(first_name, last_name, email)

    lectures = relationship("Lecture", back_populates="participants", secondary="participation")

    def __init__(self, first_name, last_name, email):
        """ Note: You could also not implement this method.
        Instances then must be initialised with keyword arguments, e.g.

        Student(first_name='Max', last_name='Mustermann', ...)

        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<Student(first_name=%s, last_name=%s, email=%s)>' \
               % (self.first_name, self.last_name, self.email)

    @classmethod
    def unique_hash(cls, first_name, last_name, email):
        return first_name, last_name, email

    @classmethod
    def unique_filter(cls, query, first_name='', last_name='', email=''):
        return query.filter(Student.email == email,
                            Student.first_name == first_name,
                            Student.last_name == last_name)
