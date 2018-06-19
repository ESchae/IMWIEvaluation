from tests.utils import DatabaseTest
from sqlalchemy.exc import IntegrityError
from student import Student


class TestStudent(DatabaseTest):

    def test_duplicate_student_not_added(self):
        s1 = Student('Max', 'Mustermann', 'max@mustermann.de')
        s2 = Student('Max', 'Mustermann', 'max@mustermann.de')
        self.session.add(s1)

        self.assertRaises(IntegrityError, self.session.add(s1))  # same object
        self.assertRaises(IntegrityError, self.session.add(s2))  # duplicate

    def test_only_mail_and_lastname_duplicated_should_add(self):
        s1 = Student('Max', 'Mustermann', 'max@mustermann.de')
        s2 = Student('Maike', 'Mustermann', 'max@mustermann.de')
        self.session.add(s1)
        self.session.add(s2)

        result = self.session.query(Student).count()
        self.assertEqual(2, result)

    def test_get_unique_existing_in_cache(self):
        """ See https://stackoverflow.com/questions/12787452/ """
        num_students_before = self.session.query(Student).count()
        s1 = Student.get_unique(  # new
            'Max', 'Mustermann', 'max@mustermann.de', self.session)
        s2 = Student.get_unique(  # taken from cache
            'Max', 'Mustermann', 'max@mustermann.de', self.session)
        num_students_after = self.session.query(Student).count()

        self.assertEqual(num_students_after, num_students_before + 1)

    def test_get_unique_existing_in_database(self):
        """ See https://stackoverflow.com/questions/12787452/ """
        num_students_before = self.session.query(Student).count()
        s1 = Student.get_unique(  # new
            'Max', 'Mustermann', 'max@mustermann.de', self.session)
        self.session.commit()  # s1 is now in database
        self.session._unique_cache.clear()  # cache is now empty
        s2 = Student.get_unique(  # taken from database
            'Max', 'Mustermann', 'max@mustermann.de', self.session)
        num_students_after = self.session.query(Student).count()

        self.assertEqual(num_students_after, num_students_before + 1)
