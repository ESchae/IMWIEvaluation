from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine('mysql+pymysql://imwi:@localhost/IMWI_Evaluation')  # connect with DB
Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()  # maintains catalog of classes and tables relative to itself
Base.metadata.create_all(engine)


def _unique(session, cls, hashfunc, queryfunc, constructor, arg, kw):
    cache = getattr(session, '_unique_cache', None)
    if cache is None:
        session._unique_cache = cache = {}

    key = (cls, hashfunc(*arg, **kw))
    if key in cache:
        return cache[key]
    else:
        with session.no_autoflush:
            q = session.query(cls)
            q = queryfunc(q, *arg, **kw)
            obj = q.first()
            if not obj:
                obj = constructor(*arg, **kw)
                session.add(obj)
        cache[key] = obj
        return obj


class UniqueMixin(object):

    @classmethod
    def __new__(cls, bases, *arg, **kw):
        # no-op __new__(), called
        # by the loading procedure
        if not arg and not kw:
            return object.__new__(cls)

        session = Session()

        def constructor(*arg, **kw):
            obj = object.__new__(cls)
            obj.__init__(*arg, **kw)
            # obj.__init__ = lambda *arg, **kw: None TODO: needed or not?
            return obj

        return _unique(
            session,
            cls,
            cls.unique_hash,
            cls.unique_filter,
            constructor,
            arg, kw
        )

    @classmethod
    def unique_hash(cls, *arg, **kw):
        raise NotImplementedError()

    @classmethod
    def unique_filter(cls, query, *arg, **kw):
        raise NotImplementedError()

