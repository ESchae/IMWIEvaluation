from sqlalchemy.orm.session import Session
from tests.database_test import DatabaseTest
from lecturer import Lecturer
from lecture import Lecture
from student import Student
from semester import Semester
from spreadsheet import SpreadsheetHandler
from unittest.mock import MagicMock


class TestLecture(DatabaseTest):

    lecture = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        session = Session(DatabaseTest.connection)
        semester = Semester('WS', 2017)
        s1 = Student('Max', 'Mustermann', 'max@mustermann.de')
        s2 = Student('Maike', 'Musterfrau', 'maike@mustermann.de')
        l1 = Lecturer('Jack', 'Johnson', 'jack@johnson.de', 'male')
        l2 = Lecturer('Jacky', 'Johnsons', 'jacky@johnson.de', 'female')
        lecture = Lecture(
            title='Learn this', tutorial=False, lecturer=l2, semester=semester)
        lecture2 = Lecture(
            title='Learn this too', tutorial=False, lecturer=l1, semester=semester)
        lecture.participants = [s1, s2]
        lecture2.participants = [s1]
        session.add_all([semester, s1, s2, l1, l2, lecture, lecture2])
        TestLecture.lecture = lecture
        session.commit()
        session.close()

    def setUp(self):
        super().setUp()
        self.lecture = self.session.query(Lecture).all()[0]
        self.lecture2 = self.session.query(Lecture).all()[1]

    """
    def test_add_participants(self):
        csv_file = 'testfiles/example_participants.csv'
        self.lecture.add_participants(csv_file, self.session)
        self.assertEqual(len(self.lecture.participants), 5)
"""
    def test_add_participant_non_existing(self):
        num_before = self.lecture.num_participants
        self.lecture.add_participant('Anna', 'Müller', 'a@x.net', self.session)
        self.assertEqual(self.lecture.num_participants, num_before + 1)

    def test_add_participant_existing(self):
        num_before = self.lecture.num_participants
        self.lecture.add_participant(
            'Max', 'Mustermann', 'max@mustermann.de', self.session)
        self.assertEqual(num_before, self.lecture.num_participants)

    def test_generate_participants_list(self):
        url = 'xyz'
        spreadsheet_handler = SpreadsheetHandler()
        spreadsheet = SpreadsheetMock(url)
        spreadsheet_handler.generate = MagicMock(return_value=spreadsheet)

        self.assertEqual(self.lecture.participant_list, None)
        self.lecture.generate_participants_list(spreadsheet_handler, self.session)
        spreadsheet_handler.generate.assert_called_with('Teilnehmer Learn this (Johnsons)')
        self.assertEqual(self.lecture.participant_list, url)
        self.assertEqual(self.lecture.evaluation_status, 'PARTICIPANT_LIST_GENERATED')


class SpreadsheetMock():

    def __init__(self, url):
        self.url = url
