"""
Copyrigh 2018
Author Elke Schaechtele

"""
from csv import DictReader

from imwievaluation.utils import clean_string


class Semester(object):

    def __init__(self, term):
        self.term = term
        self.lectures = []
        self.lecturers = []

    def read_survey_file(self, survey_file):
        with open(survey_file) as f:
            reader = DictReader(f, delimiter='\t')
            for row in reader:
                # make Lecture object and append it to self.lectures
                title = row['lecture title'].strip()
                name = row['lecturer'].strip()
                with_tutorial = row['tutorial'].strip()
                lecture = Lecture(self.term, title, name, with_tutorial)
                self.lectures.append(lecture)
                if name not in self.lecturer_names():
                    # add lecturer to self.lecturers
                    mail = row['mail'].strip()
                    gender = row['gender'].strip()
                    lecturer = Lecturer(name, mail, gender)
                    self.lecturers.append(lecturer)
                # add lecture to lecturer's lecture list
                for lecturer in self.lecturers:
                    if lecturer.name == name:
                        lecturer.add_lecture(lecture)

    def lecture_titles(self):
        lecture_titles = []
        for lecture in self.lectures:
            lecture_titles.append(lecture.title)
        return lecture_titles

    def lecturer_names(self):
        lecturer_names = []
        for lecturer in self.lecturers:
            lecturer_names.append(lecturer.name)
        return lecturer_names


class Lecturer(object):

    def __init__(self, name, mail, gender):
        self.name = name
        self.mail = mail
        self.gender = gender
        self.lectures = []

    def add_lecture(self, lecture):
        self.lectures.append(lecture)


class Lecture(object):

    def __init__(self, term, title, lecturer, with_tutorial):
        self.term = term
        self.lecturer = lecturer
        self.title = title
        self.with_tutorial = with_tutorial
        self.participants = []

    def get_evaluation_title(self):
        return 'Evaluation %s (%s) %s' % (self.title, self.lecturer, self.term)

    def get_filename(self, modus):
        lecturer = clean_string(self.lecturer)
        term = self.term.replace('/', '')  # TODO: Maybe deprecated
        if modus == 'participants':
            title = clean_string(self.title).replace(' ', '_')
            return 'Teilnehmer_%s_%s_%s.csv' % (title, lecturer, term)
        elif modus == 'csv':
            title = clean_string(self.title).replace(' ', '_')
            return 'Ergebnisse_%s_%s_%s.csv' % (title, lecturer, term)
        elif modus == 'pdf':
            title = clean_string(self.title).replace(' ', '_')
            # fileending will be added automatically in latex.py
            return 'Ergebnisse_%s_%s_%s' % (title, lecturer, term)
        elif modus == 'evaluation':
            return 'Evaluation %s (%s) %s' % (self.title, self.lecturer, term)

    def parse_participants_csv_file(self, csv_file):
        with open(csv_file) as f:
            reader = DictReader(f)
            for row in reader:
                self.participants.append({
                    'email': row['email'].strip(),
                    'lastname': row['lastname'].strip(),
                    'firstname': row['firstname'].strip()
                })
