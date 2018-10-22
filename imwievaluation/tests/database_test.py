import unittest

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

# from base import Session
from base import Base


class DatabaseTest(unittest.TestCase):
    """ Base class to inherit from when dealing with databases.

    With slight modifications taken from:
    http://alextechrants.blogspot.com/2013/08/unit-testing-sqlalchemy-apps.html

    Note: Although the article states that MySQL does not support nested
    transactions and transactional DDL, using sqlalchemy the functionality to
    have savepoints and to rollback still seems to work.

    setUp() and tearDown() methods can be overwritten, e.g. to use test
    fixtures, but remember to call the superclass implementations.

    """

    engine = None
    transaction = None
    connection = None
    test_db_url = 'mysql+pymysql://imwi:@localhost/test'

    @classmethod
    def setUpClass(cls):
        """ Connect to the db and create the schema within a transaction. """
        DatabaseTest.engine = create_engine(DatabaseTest.test_db_url)
        DatabaseTest.connection = DatabaseTest.engine.connect()
        DatabaseTest.transaction = DatabaseTest.connection.begin()
        Base.metadata.create_all(DatabaseTest.connection)  # create the tables

    @classmethod
    def tearDownClass(cls):
        """ Roll back the top level transaction and disconnect from the db. """
        DatabaseTest.transaction.rollback()
        Base.metadata.drop_all(DatabaseTest.engine)  # delete all tables
        DatabaseTest.connection.close()
        DatabaseTest.engine.dispose()

    def setUp(self):
        """ Create a savepoint to return to after every test case. """
        self.__transaction = DatabaseTest.connection.begin_nested()
        # create ad hoc session, that binds to test database
        # see http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
        # "Creating Ad-Hoc Session Objects with Alternate Arguments"
        # Session.remove()  # remove last session to prevent session conflicts
        self.session = Session(bind=DatabaseTest.connection)

    def tearDown(self):
        """ Return to save point from before last test case. """
        self.session.close()
        self.__transaction.rollback()
