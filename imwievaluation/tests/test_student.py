from tests.utils import DatabaseTest
from sqlalchemy.exc import IntegrityError
from student import Student


class TestStudent(DatabaseTest):

    def test_duplicate_student_not_added(self):
        s1 = Student('Max', 'Mustermann', 'max@mustermann.de')
        s2 = Student('Max', 'Mustermann', 'max@mustermann.de')
        self.session.add(s1)

        self.assertRaises(IntegrityError, self.session.add(s2))

    def test_only_mail_and_lastname_duplicated_should_add(self):
        s1 = Student('Max', 'Mustermann', 'max@mustermann.de')
        s2 = Student('Maike', 'Mustermann', 'max@mustermann.de')
        self.session.add(s1)
        self.session.add(s2)

        result = self.session.query(Student).count()
        self.assertEqual(2, result)
