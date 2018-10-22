from tests.database_test import DatabaseTest
from semester import Semester
from lecture import Lecture
from lecturer import Lecturer
# TODO: ugly unused imports


class TestSemeser(DatabaseTest):

    def test_unique_constraint(self):
        s1 = Semester('WS', 2014)
        s2 = Semester('WS', 2014)
        self.session.add_all([s1, s2])
        self.assertEqual(self.session.query(Semester).count(), 1)
        # TODO: needs get_unique here as well...
        # see https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/UniqueObject
        # to add get_unique for every class (maybe use class decorator)
