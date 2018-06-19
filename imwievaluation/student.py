import sqlalchemy as db
from base import Base


class Student(Base):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    # prevent duplicate entries
    db.UniqueConstraint(first_name, last_name, email)

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @classmethod
    def get_unique(cls, first_name, last_name, email, session):
        """ Alternate constructor to get a unique instance of the class.

        Checks a cache of existing uncommited instances or
        queries the database for existing commited instance
        before returning a new instance.

        Taken with modifications from:
        https://stackoverflow.com/questions/12787452/

        """
        # get the session cache, creating it if necessary
        cache = session._unique_cache = getattr(session, '_unique_cache', {})
        instance_key = (cls, first_name, last_name, email)
        instance = cache.get(instance_key)  # check if it exists in the cache
        if instance is None:  # check if it exists in the database
            instance = session.query(cls)\
                .filter_by(first_name=first_name,
                           last_name=last_name,
                           email=email)\
                .first()
            if instance is None:  # create a new instance
                instance = cls(first_name, last_name, email)
                session.add(instance)
            # update the cache
            cache[instance_key] = instance
        return instance
