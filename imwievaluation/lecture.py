import sqlalchemy as db
import csv
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
from base import Base
from student import Student
from utils import get_or_create, clean_string
from spreadsheet import SpreadsheetHandler



participation = db.Table(
    'participation', Base.metadata,
    db.Column('lecture_id', db.Integer, db.ForeignKey('lecture.id')),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    # prevent duplicate entries
    db.UniqueConstraint('lecture_id', 'student_id')
)


class Lecture(Base):
    __tablename__ = 'lecture'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tutorial = db.Column(db.Boolean, nullable=False)
    lecturer_id = db.Column(
        db.Integer, db.ForeignKey('lecturer.id'), nullable=False)
    semester_id = db.Column(
        db.Integer, db.ForeignKey('semester.id'), nullable=False)
    participants_list_url = db.Column(db.String(200), nullable=True)  # url of google spreadsheet
    evaluation_status = db.Column(mysql.ENUM(
        'LECTURE_ADDED',
        'PARTICIPANT_LIST_GENERATED'
        'PARTICIPANT_NAMES_REQUESTED',
        'PARTICIPANTS_ADDED',
        'SURVEY_GENERATED',
        'SURVEY_INVITATION_SENT',
        'SURVEY_REMINDER_SENT',
        'RESULT_SENT',
        'DISCARDED',
        'EVALUATING',
        'FINISHED'), default='LECTURE_ADDED', nullable=False)

    # prevent duplicate entries
    db.UniqueConstraint(lecturer_id, semester_id, title)

    # many to one relationship between lectures and semester
    # compare with declaration in semester.py
    semester = relationship(
        "Semester", back_populates="lectures", uselist=False)

    # many to one relationship between lectures and lecturer
    # compare with declaration in lecture.py
    lecturer = relationship(
        "Lecturer", back_populates="lectures", uselist=False)

    # many to many relationship between lecture and student
    # expressed in association table participation (see above)
    participants = relationship(
        "Student", back_populates="lectures", secondary="participation")

    def __init__(self, title, tutorial, lecturer, semester):
        self.title = title
        self.tutorial = tutorial
        self.lecturer = lecturer
        self.semester = semester

    @property
    def num_participants(self):
        return len(self.participants)

    def add_participant(self, first_name, last_name, email, session):
        participant = get_or_create(session, Student,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
        if participant not in self.participants:
            self.participants.append(participant)

    def generate_participants_list(self, spreadsheet_handler, session):
        title = 'Teilnehmer %s (%s)' % (self.title, self.lecturer.last_name)
        spreadsheet = spreadsheet_handler.generate(title)
        self.participants_list_url = spreadsheet.url
        self.evaluation_status = 'PARTICIPANT_LIST_GENERATED'
        session.commit()

    def get_filename(self, modus):
        lecturer = clean_string(self.lecturer.last_name)
        term = str(self.semester)
        if modus == 'participants':
            title = clean_string(self.title).replace(' ', '_')
            return 'Teilnehmer_%s_%s_%s.csv' % (title, lecturer, term)
        elif modus == 'csv':
            title = clean_string(self.title).replace(' ', '_')
            return 'Ergebnisse_%s_%s_%s.csv' % (title, lecturer, term)
        elif modus == 'pdf':
            title = clean_string(self.title).replace(' ', '_')
            # file ending will be added automatically in latex.py
            return 'Ergebnisse_%s_%s_%s' % (title, lecturer, term)
        elif modus == 'evaluation':
            return 'Evaluation %s (%s) %s' % (self.title, self.lecturer.last_name, term)

    # TODO: maybe deprecated (using spreadsheet now instead of csv
    def add_participants(self, csv_file, session):
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_participant(
                    row['firstname'], row['lastname'], row['email'], session)

